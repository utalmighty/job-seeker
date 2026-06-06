import requests
import csv
import os

SEARCH_TEXT = os.getenv("SEARCH_TEXT", "")
CSV_PATH = os.getenv("CSV_PATH", "./sample.csv")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", None)

class Company :
    def __init__(self, name, workday_url, location_key, locations_facets, search_text) :
        self.name = name
        self.workday_url = workday_url
        self.location_key = location_key
        self.locations = locations_facets
        self.search_text = search_text

def read_csv(file_path) :
    rows = []
    with open(file_path, "r") as f:
        data = csv.reader(f)
        for row in data :
            rows.append(row)
    return rows

def workday_search(company) :
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
    }

    json_data = {
        'appliedFacets': {company.location_key: company.locations},
        'limit': 20, 'offset': 0, 'searchText': company.search_text
    }

    response = requests.post(company.workday_url, headers=headers, json=json_data)

    return response.json()

def discord_notification(message) :
    if (DISCORD_WEBHOOK == None) :
        return
    
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
    }

    json_data = {
        "content" : message
    }

    requests.post(url=DISCORD_WEBHOOK, json=json_data, headers=headers)

def search_job(company, POSTED_DAY = "today") :
    resp = workday_search(company)
    postings = resp["jobPostings"]
    for posting in postings :
        postedOn = posting["postedOn"]
        if POSTED_DAY.lower() in postedOn.lower() :
            bulletFields = posting["bulletFields"]
            ping = "**" + company.name + "** posted job with keyword *" + company.search_text + "* Job ID: `" + str(bulletFields) + "`"
            discord_notification(ping)

if __name__ == "__main__" :

    rows = read_csv(CSV_PATH)

    for row in rows :
        name = row[0].strip()
        url = row[1].strip()
        location_key = row[2].strip()
        locations = []
        for location in row[3:] :
            locations.append(location.strip())
        company = Company(name, url, location_key, locations, SEARCH_TEXT)
        search_job(company)