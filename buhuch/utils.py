import re

import requests
from bs4 import BeautifulSoup as bs

from settings import HEADERS, MIN_SALARY_LINK


def scrape_min_salary(year: int) -> float:
    """
    Scrape min salary by year

    :param year: Year
    :return min_salary: Minimal salary for provided year
    """
    response: requests.Response = requests.get(url=MIN_SALARY_LINK, headers=HEADERS)
    soup = bs(response.content, "lxml")

    table = soup.find("table", attrs={"class": "table"})
    trs = table.find_all("tr")

    for tr in trs[1:]:
        tds = tr.find_all("td")
        min_salary_text = tds[0].text.strip()

        if str(year) in min_salary_text:
            min_salary_value = re.findall(r".*-\s([\d\w\s]+)\s\D+$", min_salary_text)
            return float(min_salary_value[0].replace(" ", ""))

    return 0
