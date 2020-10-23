from datetime import datetime

import pytest

from hestia.bills.datatypes import SalaryTaxSchema
from hestia.swagger import SalaryTaxCalculatorMixin


@pytest.fixture
def mock_datetime(mocker):
    mock_datetime = mocker.patch("hestia.swagger.datetime")
    mock_datetime.now.return_value = datetime(2020, 1, 1, 14, 0)
    return mock_datetime


@pytest.fixture
def mock_scrape_min_salary(mocker):
    mock_scrape_min_salary = mocker.patch("hestia.swagger.scrape_min_salary")
    mock_scrape_min_salary.return_value = 42500
    return mock_scrape_min_salary


@pytest.fixture
def tax_calculator(mock_datetime, mock_scrape_min_salary):
    return SalaryTaxCalculatorMixin(salary=60000)


def test_superannuation(tax_calculator: SalaryTaxCalculatorMixin):
    superannuation_value, superannuation_schema = tax_calculator.superannuation()
    assert superannuation_value == 6000
    assert isinstance(superannuation_schema, SalaryTaxSchema)


def test_corrections(
    tax_calculator: SalaryTaxCalculatorMixin,
):
    assert tax_calculator.corrections() == 10350


def test_personal_income_tax(tax_calculator: SalaryTaxCalculatorMixin):
    (
        personal_income_tax_value,
        personal_income_tax_schema,
    ) = tax_calculator.personal_income_tax()
    assert personal_income_tax_value == 115
    assert isinstance(personal_income_tax_schema, SalaryTaxSchema)


def test_health_insurance(tax_calculator: SalaryTaxCalculatorMixin):
    health_insurance_value, health_insurance_schema = tax_calculator.health_insurance()
    assert health_insurance_value == 600
    assert isinstance(health_insurance_schema, SalaryTaxSchema)


def test_social_contributions(tax_calculator: SalaryTaxCalculatorMixin):
    (
        social_contributions_value,
        social_contributions_schema,
    ) = tax_calculator.social_contributions()
    assert round(social_contributions_value, 2) == 1890
    assert isinstance(social_contributions_schema, SalaryTaxSchema)


def test_social_deductions(tax_calculator: SalaryTaxCalculatorMixin):
    (
        social_deductions_value,
        social_deductions_schema,
    ) = tax_calculator.social_deductions()
    assert social_deductions_value == 3183
    assert isinstance(social_deductions_schema, SalaryTaxSchema)


def test_compulsory_social_health_insurance(tax_calculator: SalaryTaxCalculatorMixin):
    (
        compulsory_social_health_insurance_value,
        compulsory_social_health_insurance_schema,
    ) = tax_calculator.compulsory_health_insurance()
    assert compulsory_social_health_insurance_value == 1200
    assert isinstance(compulsory_social_health_insurance_schema, SalaryTaxSchema)


def test_superannuation_employer(tax_calculator: SalaryTaxCalculatorMixin):
    (
        superannuation_employer_value,
        superannuation_employer_schema,
    ) = tax_calculator.superannuation_employer()
    assert superannuation_employer_value == 3000
    assert isinstance(superannuation_employer_schema, SalaryTaxSchema)


def test_find_final_salary(
    tax_calculator: SalaryTaxCalculatorMixin,
):
    final, schema = tax_calculator.find_final_salary()

    assert final == 53285
    assert schema == {
        "social_deductions": {
            "value": 3183.0,
            "schema": {"debit": 7210, "credit": 3240},
        },
        "compulsory_social_health_insurance": {
            "value": 1200.0,
            "schema": {"debit": 7210, "credit": 3240},
        },
        "social_contributions": {
            "value": 1890.0000000000002,
            "schema": {"debit": 7210, "credit": 3150},
        },
        "health_insurance": {"value": 600.0, "schema": {"debit": 3350, "credit": 3240}},
        "superannuation": {"value": 6000.0, "schema": {"debit": 3350, "credit": 3220}},
        "personal_income_tax": {
            "value": 115.0,
            "schema": {"debit": 3850, "credit": 3350},
        },
        "superannuation_employer": {
            "schema": {"debit": 3350, "credit": 3220},
            "value": 3000.0,
        },
    }
