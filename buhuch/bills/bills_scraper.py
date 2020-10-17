"""
Bills scraper
~~~~~~~~~~~~~

This module provides the bills scraper

Usage:
    >>> from buhuch.bills.bills_scraper import BillsScraper
    >>> scraper = BillsScraper(filename="my_bills")  # it's optional arg.
    >>> data = scraper.get_bills()  # Scrape the bills
    >>> scraper.save(data)  # Save it in json file which you set before
"""
import dataclasses
import json
from typing import Dict, Optional, Union

import requests
from bs4 import BeautifulSoup as bs

from settings import BASE_DIR, BILLS_SITE_URL, HEADERS

from .datatypes import Bill, BillItem, BillsList


class BillsScraper:
    def __init__(self, filename: str = f"{BASE_DIR}/bills.json") -> None:
        self.filename = filename

    def save(self, bills: BillsList) -> None:  # pragma: no cover
        """
        Save bills in json file in json format

        :param bills: BillsList type object
        """
        bills_json = []
        for bill in bills:
            bills_json.append(dataclasses.asdict(bill))

        with open(self.filename, "w+") as f:
            f.truncate()
            json.dump(bills_json, f, ensure_ascii=False, indent=4)

    def parse_html(self, content: bytes) -> BillsList:
        """
        Parse html of web page

        :param content: Byte strings of web page
        :return parsed_bills: BillsList type object
        """
        soup = bs(content, "lxml")
        bills_list = soup.find("tbody").find_all("tr")

        parsed_bills: BillsList = []
        is_topic = 0
        temp_info: Dict[str, Union[str, int]] = {}

        for bill in bills_list:
            tds = bill.find_all("td")

            if len(tds) > 1:
                temp_index: int = int(temp_info["index"])

                parsed_bills[temp_index].bills.append(
                    Bill(
                        title=tds[1]
                        .text.strip()
                        .replace("\r\n ", "")
                        .replace("\n ", ""),
                        bill=tds[0]
                        .text.strip()
                        .replace("\r\n ", "")
                        .replace("\n ", ""),
                    )
                )

            elif len(tds) == 1:
                temp_info.update(
                    {
                        "topic": tds[0].text.strip(),
                        "index": is_topic,
                    }
                )
                parsed_bills.append(BillItem(topic=str(temp_info["topic"]), bills=[]))
                is_topic += 1

        return parsed_bills

    def get_bills(self) -> Optional[BillsList]:
        """
        Scrape web page
        :return content: BillsList type object
        """
        response: requests.Response = requests.get(url=BILLS_SITE_URL, headers=HEADERS)

        if response.status_code == 200:
            content: BillsList = self.parse_html(response.content)
            return content
        else:  # pragma: no cover
            raise ValueError(f"Status code is not 200 | {response.status_code}")
