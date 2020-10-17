from unittest.mock import Mock

import pytest

from buhuch.bills.bills_scraper import BillsScraper


@pytest.fixture
def mock_bills_requests_get(mocker, helpers):
    mock_bills_requests_get = Mock()
    mock_bills_requests_get.return_value.status_code = 200
    mock_bills_requests_get.return_value.content = helpers.txt_to_bytes(
        "samples/bills_response_example.txt"
    )
    return mock_bills_requests_get


@pytest.fixture
def mock_bills_requests(mocker, mock_bills_requests_get):
    mock_bills_requests = mocker.patch("buhuch.bills.bills_scraper.requests")
    mock_bills_requests.get = mock_bills_requests_get
    return mock_bills_requests


@pytest.fixture
def bills_scraper():
    return BillsScraper()


def test_get_bill(mock_bills_requests, mock_bills_requests_get, bills_scraper, helpers):
    bills = bills_scraper.get_bills()
    json_bills = helpers.bills_list_to_dict(bills)
    expected_json = helpers.read_json("samples/bills.json")

    assert json_bills == expected_json


def test_parse_html(bills_scraper, helpers):
    bills = bills_scraper.parse_html(
        content=helpers.txt_to_bytes("samples/bills_response_example.txt")
    )
    json_bills = helpers.bills_list_to_dict(bills)
    expected_json = helpers.read_json("samples/bills.json")

    assert json_bills == expected_json
