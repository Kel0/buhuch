import pytest

from hestia.utils import scrape_min_salary


@pytest.fixture
def mock_requests(mocker, helpers):
    mock_requests = mocker.patch("hestia.utils.requests")
    mock_requests.get.return_value.status_code = 200
    mock_requests.get.return_value.content = helpers.txt_to_bytes(
        "samples/min_salary_response.txt"
    )
    return mock_requests


def test_scrape_min_salary(mock_requests):
    salary = scrape_min_salary(year=2020)

    assert salary == 42500
