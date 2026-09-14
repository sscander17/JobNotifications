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
    }
]
