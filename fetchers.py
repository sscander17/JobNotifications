import requests
from bs4 import BeautifulSoup


def fetch_greenhouse(company):
    url = f"https://boards-api.greenhouse.io/v1/boards/{company['id_or_url']}/jobs"
    response = requests.get(url)
    response.raise_for_status()
    jobs = response.json().get("jobs", [])

    location_filter = company.get("location")
    filtered = {}
    for job in jobs:
        if location_filter:
            job_location = job.get("location", {}).get("name", "")
            if location_filter.lower() not in job_location.lower():
                continue
        filtered[job["absolute_url"]] = job["title"]
    return filtered


def fetch_eightfold(company):
    career_site = company["career_site"]
    domain = company.get("domain", career_site)
    location_filter = company.get("location", "")

    url = f"https://{career_site}/api/apply/v2/jobs"

    # Spoof a real Google Chrome browser to bypass the 403 Firewall
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"https://{career_site}/careers",
        "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

    filtered_jobs = {}
    start = 0
    num = 100

    while True:
        params = {
            "domain": domain,
            "start": start,
            "num": num,
            "location": location_filter
        }

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()
        positions = data.get("positions", [])

        if not positions:
            break

        for job in positions:
            job_id = job.get("id")
            title = job.get("name", "Unknown Title")
            full_url = f"https://{career_site}/careers?pid={job_id}"
            filtered_jobs[full_url] = title

        total_count = data.get("count", 0)
        if start + len(positions) >= total_count or len(positions) == 0:
            break

        start += num

    return filtered_jobs

def fetch_recruitee(company):
    url = f"https://{company['subdomain']}.recruitee.com/api/offers/"
    response = requests.get(url)
    response.raise_for_status()
    jobs = response.json().get("offers", [])
    return {job["careers_url"]: job["title"] for job in jobs if "careers_url" in job}


def fetch_workday(company):
    tenant = company["tenant"]
    career_site = company["career_site"]
    location_facet = company.get("location_facet")
    url = f"https://{tenant}.wd3.myworkdayjobs.com/wday/cxs/{tenant}/{career_site}/jobs"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    filtered_jobs = {}
    offset = 0
    while True:
        payload = {
            "appliedFacets": {"locations": [location_facet]} if location_facet else {},
            "limit": 20,
            "offset": offset,
            "searchText": ""
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        jobs = response.json().get("jobPostings", [])

        for job in jobs:
            full_url = f"https://{tenant}.wd3.myworkdayjobs.com/en-US/{career_site}{job['externalPath']}"
            filtered_jobs[full_url] = job["title"]

        if len(jobs) < 20:
            break
        offset += 20

    return filtered_jobs


def fetch_scrape(company):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(company["url"], headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    current_jobs = {}
    for link in soup.find_all('a'):
        href = link.get('href')
        title = link.get_text(strip=True)
        if href and company["url_filter"] in href and title:
            if title.lower() not in ["view job", "apply now", "read more"]:
                if not href.startswith("http"):
                    href = company["url"].rstrip("/") + href
                current_jobs[href] = title
    return current_jobs


# Registry maps 'type' string directly to the function
FETCHERS = {
    "greenhouse": fetch_greenhouse,
    "recruitee": fetch_recruitee,
    "workday": fetch_workday,
    "scrape": fetch_scrape,
    "eightfold": fetch_eightfold, # <--- Updated
}