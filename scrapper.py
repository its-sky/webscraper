import requests
from bs4 import BeautifulSoup


def get_last_page(URL):
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
  last_page = pages[-2].get_text().strip()
  return int(last_page)


def extract_job(html):
  title = html.find("a", {"class": "s-link"})["title"]

  company = html.find("h3", {"class": "fc-black-700"}).find("span").get_text(strip=True)

  location = html.find("h3", {"class": "fc-black-700"}).find("span", {"class": "fc-black-500"}).get_text(strip=True)

  job_id = html['data-jobid']

  return {
      'title': title,
      'company': company,
      'location': location,
      'link': f"https://stackoverflow.com/jobs/{job_id}/"
  }


def extract_jobs(last_page, URL):
  jobs = []
  for page in range(last_page):
    print(f"SO {page+1}페이지 추출 완료")
    result = requests.get(f"{URL}&pg={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "-job"})

    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs


def get_jobs(word):
  URL = f"https://stackoverflow.com/jobs?q={word}"
  last_page = get_last_page(URL)
  jobs = extract_jobs(last_page, URL)
  return jobs
