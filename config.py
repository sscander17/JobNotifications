STATE_FILE = "saved_jobs.json"

COMPANIES = [
    {
        "name": "Helsing",
        "type": "greenhouse",
        "id_or_url": "helsing"
    },
    {
        "name": "ARX Robotics",
        "type": "greenhouse",
        "id_or_url": "arxroboticsgmbh",
        "location": "Munich"
    },
    {
        "name": "TYTAN Technologies",
        "type": "recruitee",
        "subdomain": "tytantechnologiesgmbh"
    },
    {
        "name": "Samsung",
        "type": "workday",
        "tenant": "sec",
        "career_site": "Samsung_Careers",
        "location_facet": "39065a4e567f0126a5c0e8b862498003"
    },
    {
        "name": "Quantum-Systems",
        "type": "scrape",
        "url": "https://career.quantum-systems.com/",
        "url_filter": "/o/"
    },
    {
        "name": "Qualcomm",
        "type": "eightfold",
        "career_site": "careers.qualcomm.com",
        "domain": "qualcomm.com",
        "location": "Munich"
    },
    {
        "name": "Isar Aerospace",
        "type": "greenhouse",
        "id_or_url": "isaraerospace",
        "location": "Ottobrunn" # Their main facility location just outside Munich
    },
    {
        "name": "Infineon",
        "type": "eightfold",
        "career_site": "jobs.infineon.com",
        "domain": "infineon.com",
        "location": "Munich"
    },
    {
        "name": "Alpine Eagle",
        "type": "greenhouse",
        "id_or_url": "alpineeagle",
        "location": ["Munich", "München"]  # <--- Accepts both!
    },
    {
        "name": "Siemens",
        "type": "avature",
        "url": "https://jobs.siemens.com/en_US/externaljobs/SearchJobs/?42386=%5B812132%5D&42386_format=17546&42387=%5B813141%5D&42387_format=17547&42388=%5B912803%5D&42388_format=17879&42389=%5B102117%2C39106405%2C102127%5D&42389_format=17549&listFilterMode=1&folderRecordsPerPage=100&"
    },
    {
        "name": "DLR",
        "type": "dlr",
        "location": "Oberpfaffenhofen"
    },
    {
        "name": "Hive Robotics",
        "type": "personio",
        "subdomain": "hive-robotics"
    },
    {
        "name": "Airbus",
        "type": "workday",
        "tenant": "ag",
        "career_site": "Airbus",
        "location_facet": [
            "f5811cef9cb501a49eac0a694c0a8244",
            "f5811cef9cb50199bf69196b4c0a674b"
        ]
    },
    {
        "name": "NXP Semiconductors",
        "type": "workday",
        "tenant": "nxp",
        "career_site": "careers",
        "location_facet": "3db468d56aa610d69085a48b83d7492d"
    },
    {
        "name": "Texas Instruments",
        "type": "oraclecloud",
        "base_url": "https://careers.ti.com/en/sites/CX",
        "api_url": "https://edbz.fa.us2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions",
        "site_number": "CX",
        "location_id": "100001733959266"
    },
    {
        "name": "Intel",
        "type": "workday",
        "tenant": "intel",
        "wd_server": "wd1",
        "career_site": "External",
        "location_facet": "1e4a4eb3adf101311d06d076bf815ccf"
    },
    {
        "name": "Analog Devices",
        "type": "workday",
        "tenant": "analogdevices",
        "wd_server": "wd1",
        "career_site": "External",
        "location_facet": [
            "633b03df4f5d1000e7e5c5dff3800000",
            "c057160fc3ff10010d4a00c83f920000"
        ]
    },
    {
        "name": "Engineering Minds Munich",
        "type": "em_munich",
        "url": "https://www.em-munich.de/career"
    },
    {
        "name": "AMD",
        "type": "jibe",
        "api_url": "https://careers.amd.com/api/jobs",
        "base_job_url": "https://careers.amd.com/careers-home/jobs",
        "location": "Munich, Germany"
    },
    {
        "name": "BMW Group",
        "type": "bmw",
        "location_filter": "munich"
    },
    {
        "name": "Stark Defence",
        "type": "personio",
        "subdomain": "stark",
        "location_filter": "munich"
    }
]
