import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=pytho&sort=i"

# 1. get the page
# 2. make the request
# 3. extract the jobs


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")  # soup -> Local Variable
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    title = html.find("a", {"class", "s-link"})["title"]
    company, location = html.find(
        "h3", {"class", "fc-black-700"}).find_all("span", recursive=False)  # recursive=False
    company = company.get_text(strip=True)
    location = location.get_text(strip=True).strip("-").strip("\r").strip("\n")
    return {"title": title, "company": company, "location": location}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs