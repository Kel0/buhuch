from datetime import datetime

import pytest

from buhuch.swagger import SalaryTaxCalculatorMixin


@pytest.fixture
def mock_datetime(mocker):
    mock_datetime = mocker.patch("buhuch.swagger.datetime")
    mock_datetime.now.return_value = datetime(2020, 1, 1, 14, 0)
    return mock_datetime


@pytest.fixture
def mock_scrape_min_salary(mocker):
    mock_scrape_min_salary = mocker.patch("buhuch.swagger.scrape_min_salary")
    mock_scrape_min_salary.return_value = 42500
    return mock_scrape_min_salary


@pytest.fixture
def tax_calculator(mock_datetime, mock_scrape_min_salary):
    return SalaryTaxCalculatorMixin(salary=60000)


def test_superannuation(tax_calculator: SalaryTaxCalculatorMixin):
    assert tax_calculator.superannuation() == 6000


def test_corrections_salary_superannuation_min_salary(
    tax_calculator: SalaryTaxCalculatorMixin,
):
    assert tax_calculator.corrections_salary_superannuation_min_salary() == 10350


def test_personal_income_tax(tax_calculator: SalaryTaxCalculatorMixin):
    assert tax_calculator.personal_income_tax() == 115


def test_health_insurance(tax_calculator: SalaryTaxCalculatorMixin):
    assert tax_calculator.health_insurance() == 600


def test_social_contributions(tax_calculator: SalaryTaxCalculatorMixin):
    assert round(tax_calculator.social_contributions(), 2) == 1890


def test_social_receives(tax_calculator: SalaryTaxCalculatorMixin):
    assert tax_calculator.social_receives() == 3183


def test_compulsory_social_health_insurance(tax_calculator: SalaryTaxCalculatorMixin):
    assert tax_calculator.compulsory_social_health_insurance() == 1200
