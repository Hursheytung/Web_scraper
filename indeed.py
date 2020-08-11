import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit={LIMIT}"

def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')

    pagination = soup.find("div", {"class": 'pagination'})

    links = pagination.find_all('a')
    pages = []
    for link in links[0:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    #result=html 전체 페이지 title이라는 class에서 anchor에 있는 title만 extract
    company = html.find("span", {"class": "company"})  #soup
    if company:
        company_anchor = company.find("a")
        #soup's results
        if company_anchor is not None:
            company = str(company_anchor.
                          string)  #comapny has a link just print company name
        else:
            company = str(company.string)
            #str func make no spaces in the result
            #company hasn't a link
        company = company.strip()  #remove space
    else:
        company = None
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    #location = div["data-re-loc"]
    #location = html.find("span", {"class": "location accessible-contrast-color-location"}).string -none값이 없을경우
    job_id = html["data-jk"]
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://kr.indeed.com/viewjob?jk={job_id}"
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scarpping page {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
