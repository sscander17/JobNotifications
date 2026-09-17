import requests
from bs4 import BeautifulSoup


def fetch_avature(company):
    base_url = company["url"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    filtered_jobs = {}
    offset = 0

    while True:
        # Dynamically append the offset parameter to the base URL
        separator = "&" if "?" in base_url else "?"
        paginated_url = f"{base_url}{separator}folderOffset={offset}"

        response = requests.get(paginated_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        job_headers = soup.find_all("h3", class_="article__header__text__title")

        # Stop looping if a page has no job listings
        if not job_headers:
            break

        for header in job_headers:
            link_tag = header.find("a")
            if link_tag and link_tag.has_attr("href"):
                job_url = link_tag["href"]
                job_title = link_tag.get_text(strip=True)

                if job_url.startswith("http"):
                    filtered_jobs[job_url] = job_title

        # If the page returns fewer jobs than the expected limit, it is the last page
        if len(job_headers) < 6:
            break

        # Increment the offset by the number of jobs found (usually 6) to fetch the next page
        offset += len(job_headers)

    return filtered_jobs


def fetch_greenhouse(company):
    board_token = company["id_or_url"]
    location_filter = company.get("location")

    url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    filtered_jobs = {}

    # Convert location_filter into a clean list of lowercase keywords
    if isinstance(location_filter, str):
        target_locations = [location_filter.lower()]
    elif isinstance(location_filter, list):
        target_locations = [loc.lower() for loc in location_filter]
    else:
        target_locations = []

    for job in data.get("jobs", []):
        job_location = job.get("location", {}).get("name", "")

        # If a filter exists, ensure at least ONE keyword matches the job location
        if target_locations:
            if not any(loc in job_location.lower() for loc in target_locations):
                continue

        filtered_jobs[job["absolute_url"]] = job["title"]

    return filtered_jobs


def fetch_eightfold(company):
    import re
    import urllib.parse
    
    career_site = company["career_site"]
    location_filter = company.get("location", "").lower()
    
    # We use the sitemap approach to bypass Cloudflare 403 on the API
    url = f"https://{career_site}/careers/sitemap.xml"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Warning: Could not fetch sitemap for {career_site}")
        return {}

    urls = re.findall(r'<loc>(.*?)</loc>', response.text)
    
    # Simple heuristic to extract the main city name for filtering the URL slug
    primary_location_word = location_filter.split(',')[0].strip() if location_filter else ""
    
    filtered_jobs = {}
    
    for job_url in urls:
        if '/job/' not in job_url:
            continue
            
        decoded_url = urllib.parse.unquote(job_url)
        if primary_location_word and primary_location_word not in decoded_url.lower():
            continue
            
        # The URL structure is typically .../job/123456-job-title-slug
        parts = decoded_url.rstrip('/').split('/')
        slug_part = parts[-1]
        
        # Remove the ID prefix (e.g., 446720790054-)
        title_slug = re.sub(r'^\d+-', '', slug_part)
        # Strip query parameters if present
        title_slug = title_slug.split('?')[0]
        
        # Format the title slug into a readable title
        words = title_slug.replace('-', ' ').split()
        clean_title = " ".join(word.capitalize() for word in words)
        
        filtered_jobs[job_url] = clean_title
            
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
    wd_server = company.get("wd_server", "wd3")
    location_facet = company.get("location_facet")
    url = f"https://{tenant}.{wd_server}.myworkdayjobs.com/wday/cxs/{tenant}/{career_site}/jobs"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    filtered_jobs = {}
    offset = 0
    while True:
        locations_list = location_facet if isinstance(location_facet, list) else [location_facet]
        payload = {
            "appliedFacets": {"locations": locations_list} if location_facet else {},
            "limit": 20,
            "offset": offset,
            "searchText": ""
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        jobs = response.json().get("jobPostings", [])

        for job in jobs:
            full_url = f"https://{tenant}.{wd_server}.myworkdayjobs.com/en-US/{career_site}{job['externalPath']}"
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


def fetch_dlr(company):
    import re
    from urllib.parse import unquote

    url = "https://jobs.dlr.de/sitemap.xml"
    response = requests.get(url)
    response.raise_for_status()

    urls = re.findall(r'<loc>(https://jobs\.dlr\.de/job/[^<]+)</loc>', response.text)

    filtered_jobs = {}
    location_filter = company.get("location", "").lower()

    for job_url in urls:
        parts = job_url.rstrip('/').split('/')
        if len(parts) >= 2:
            slug = unquote(parts[-2])
            title = slug.replace('-', ' ')

            if location_filter and location_filter not in title.lower():
                continue

            filtered_jobs[job_url] = title

    return filtered_jobs


def fetch_personio(company):
    import re
    import html
    subdomain = company["subdomain"]
    url = f"https://{subdomain}.jobs.personio.com/xml"
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = 'utf-8'

    location_filter = company.get("location_filter", "").lower()
    positions = re.findall(r'<position>(.*?)</position>', response.text, re.DOTALL)
    
    filtered_jobs = {}
    for pos in positions:
        id_match = re.search(r'<id>([^<]+)</id>', pos)
        name_match = re.search(r'<name><!\[CDATA\[(.*?)\]\]></name>', pos) or re.search(r'<name>([^<]+)</name>', pos)
        
        office_match = re.search(r'<office>([^<]+)</office>', pos)
        office_cdata = re.search(r'<office><!\[CDATA\[(.*?)\]\]></office>', pos)
        desc_match = re.search(r'<jobDescriptions>(.*?)</jobDescriptions>', pos, re.DOTALL)
        
        office = office_cdata.group(1) if office_cdata else (office_match.group(1) if office_match else "")
        desc = desc_match.group(1) if desc_match else ""
        
        job_location = office.lower()
        job_desc = desc.lower()
        
        if location_filter:
            if location_filter not in job_location and location_filter not in job_desc:
                continue
        
        if id_match and name_match:
            job_id = id_match.group(1).strip()
            job_title = html.unescape(name_match.group(1).strip())
            job_url = f"https://{subdomain}.jobs.personio.com/job/{job_id}"
            filtered_jobs[job_url] = job_title
            
    return filtered_jobs


# Registry maps 'type' string directly to the function
def fetch_oraclecloud(company):
    api_url = company["api_url"]
    base_url = company["base_url"]
    site_number = company.get("site_number", "CX")
    location_id = company.get("location_id")
    
    finder = f"findReqs;siteNumber={site_number}"
    if location_id:
        finder += f",locationId={location_id}"
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    filtered_jobs = {}
    offset = 0
    
    while True:
        params = {
            "onlyData": "true",
            "expand": "requisitionList.secondaryLocations,flexFieldsFacet.values",
            "finder": finder,
            "offset": offset
        }
        try:
            response = requests.get(api_url, params=params, headers=headers, timeout=10)
            if response.status_code != 200:
                break
                
            data = response.json()
            items = data.get("items", [])
            if not items:
                break
                
            requisitions = items[0].get("requisitionList", [])
            if not requisitions:
                break
                
            for job in requisitions:
                job_id = job.get("Id")
                title = job.get("Title", "Unknown Title")
                # e.g. https://careers.ti.com/en/sites/CX/job/25001591/
                full_url = f"{base_url}/job/{job_id}/"
                filtered_jobs[full_url] = title
                
            if offset + len(requisitions) >= items[0].get("TotalJobsCount", 0):
                break
                
            offset += len(requisitions)
        except Exception:
            break
            
    return filtered_jobs

def fetch_em_munich(company):
    url = company["url"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    filtered_jobs = {}

    for a_tag in soup.find_all("a", href=True):
        link = a_tag["href"]
        if ".pdf" not in link:
            continue
            
        try:
            parent1 = a_tag.find_parent("div")
            if not parent1: continue
            parent2 = parent1.find_parent("div")
            if not parent2: continue
            
            title = parent2.get_text(separator=" ", strip=True).replace("Up", "").strip()
            
            if title and link not in filtered_jobs:
                filtered_jobs[link] = title
        except Exception:
            pass

    return filtered_jobs

def fetch_jibe(company):
    api_url = company["api_url"]
    base_job_url = company["base_job_url"]
    location = company.get("location")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    filtered_jobs = {}
    page = 1
    
    while True:
        params = {
            "page": page,
            "limit": 100
        }
        if location:
            params["location"] = location
            
        try:
            response = requests.get(api_url, params=params, headers=headers, timeout=10)
            if response.status_code != 200:
                break
                
            data = response.json()
            jobs = data.get("jobs", [])
            if not jobs:
                break
                
            for job in jobs:
                job_data = job.get("data", {})
                req_id = job_data.get("req_id")
                title = job_data.get("title", "Unknown Title")
                
                if req_id:
                    full_url = f"{base_job_url}/{req_id}"
                    filtered_jobs[full_url] = title
                    
            if len(jobs) < 100:
                break
                
            page += 1
        except Exception:
            break
            
    return filtered_jobs

def fetch_bmw(company):
    import time
    from curl_cffi import requests as curl_requests
    url = "https://www.bmwgroup.jobs/en/_jcr_content/main/layoutcontainer_5337/jobfinder30.jobfinder_table.content.html"
    base_domain = "https://www.bmwgroup.jobs"
    location_filter = company.get("location_filter", "").lower()

    for attempt in range(3):
        try:
            response = curl_requests.get(url, impersonate="chrome110", timeout=60)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")
            response.encoding = 'utf-8'
            break
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(5)

    soup = BeautifulSoup(response.text, "html.parser")
    filtered_jobs = {}

    for wrapper in soup.find_all("div", class_="grp-jobfinder__wrapper"):
        a_tag = wrapper.find("a", class_="grp-jobfinder__link-jobdescription")
        if not a_tag:
            continue
            
        link = a_tag["href"]
        if link.startswith("/"):
            link = base_domain + link
            
        refno_div = wrapper.find("div", class_="grp-jobfinder-cell-refno")
        if not refno_div:
            continue
            
        job_location = refno_div.get("data-job-location", "").lower()
        job_title = refno_div.get("data-job-title", "Unknown Title")
        
        if location_filter and location_filter not in job_location:
            continue
            
        filtered_jobs[link] = job_title

    return filtered_jobs

def fetch_renesas(company):
    from curl_cffi import requests as curl_requests
    import time
    
    url_template = company["url_template"]
    base_domain = company.get("base_domain", "https://jobs.renesas.com")
    
    filtered_jobs = {}
    
    for page in range(1, 20):
        url = url_template.format(page)
        
        for attempt in range(3):
            try:
                response = curl_requests.get(url, impersonate="chrome110", timeout=60)
                if response.status_code != 200:
                    raise Exception(f"HTTP {response.status_code}")
                response.encoding = 'utf-8'
                break
            except Exception as e:
                if attempt == 2:
                    raise
                time.sleep(5)
        
        soup = BeautifulSoup(response.text, "html.parser")
        new_jobs = 0
        
        for a in soup.find_all('a', href=True):
            if '/job/' in a['href'] and a.text.strip() and a.text.strip() != 'View job':
                link = base_domain + a['href'] if a['href'].startswith('/') else a['href']
                if link not in filtered_jobs:
                    filtered_jobs[link] = a.text.strip()
                    new_jobs += 1
                    
        if new_jobs == 0:
            break
            
    return filtered_jobs

FETCHERS = {
    "greenhouse": fetch_greenhouse,
    "workday": fetch_workday,
    "scrape": fetch_scrape,
    "recruitee": fetch_recruitee,
    "eightfold": fetch_eightfold,
    "avature": fetch_avature,
    "dlr": fetch_dlr,
    "personio": fetch_personio,
    "oraclecloud": fetch_oraclecloud,
    "em_munich": fetch_em_munich,
    "jibe": fetch_jibe,
    "bmw": fetch_bmw,
    "renesas": fetch_renesas
}