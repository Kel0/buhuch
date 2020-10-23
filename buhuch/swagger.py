from datetime import datetime
from typing import Tuple

from .utils import scrape_min_salary

from .bills.datatypes import (  # isort:skip
    SalaryTaxCalculatorMixinBillsAlias,
    SalaryTaxSchema,
)


class SalaryTaxCalculatorMixin:
    def __init__(
        self,
        salary: float = 0,
        year: int = datetime.now().year,
    ) -> None:
        self.salary = salary
        self.min_salary = scrape_min_salary(year)
        self.alias_mixin = SalaryTaxCalculatorMixinBillsAlias()

    def superannuation(self) -> Tuple[float, SalaryTaxSchema]:
        """
        Superannuation calculation formula:
            salary * 10%
        :return superannuation: Superannuation value
        """
        superannuation = self.salary * 0.1
        return superannuation, self.alias_mixin.superannuation

    def corrections(self) -> float:
        """
        Salary corrections calculation formula:
            (salary - superannuation - min_salary) * 90%
        :return corrections_value: Correction value
        """
        superannuation_value, _ = self.superannuation()
        corrections_value = (self.salary - superannuation_value - self.min_salary) * 0.9
        return corrections_value

    def personal_income_tax(self) -> Tuple[float, SalaryTaxSchema]:
        """
        Personal income tax calculation formula:
            (salary - superannuation - min_salary - corrections) * 10%
        :return income_value: Income tax value
        """
        corrections_value: float = 0
        if self.salary < 65500:
            corrections_value = self.corrections()
        superannuation_value, _ = self.superannuation()

        income_value = (
            self.salary - superannuation_value - self.min_salary - corrections_value
        ) * 0.1
        return income_value, self.alias_mixin.personal_income_tax

    def health_insurance(self) -> Tuple[float, SalaryTaxSchema]:
        """
        Formula for calculate health insurance tax formula:
            (salary * 0.01)
        :return health_insurance_value: Price of health insurance
        """
        health_insurance_value = self.salary * 0.01
        return health_insurance_value, self.alias_mixin.health_insurance

    def social_contributions(self) -> Tuple[float, SalaryTaxSchema]:
        """
        Formula for calculate social contributions tax formula:
            (salary - superannuation) * 0.035
        :return social_contributions_value: Price of health insurance
        """
        superannuation_value, _ = self.superannuation()
        social_contributions_value = (self.salary - superannuation_value) * 0.035
        return social_contributions_value, self.alias_mixin.social_contributions

    def social_deductions(self) -> Tuple[float, SalaryTaxSchema]:
        """
        Formula for calculate social deductions formula:
            (salary - superannuation - health_insurance) * 0.095 - social_contributions
        :return social_deductions_value: Social receives value
        """
        superannuation_value, _ = self.superannuation()
        social_contributions_value, _ = self.social_contributions()
        health_insurance_value, _ = self.health_insurance()

        social_deductions_value = (
            self.salary - superannuation_value - health_insurance_value
        ) * 0.095 - social_contributions_value
        return social_deductions_value, self.alias_mixin.social_deductions

    def compulsory_health_insurance(self) -> Tuple[float, SalaryTaxSchema]:
        """
        Formula for calculate compulsory health insurance formula:
            (salary * 0.02)
        :return compulsory_health_insurance_value: Compulsory social health insurance value
        """
        compulsory_health_insurance_value = self.salary * 0.02
        return (
            compulsory_health_insurance_value,
            self.alias_mixin.compulsory_health_insurance_value,
        )

    def find_final_salary(self, as_dict: bool = True) -> Tuple[float, dict]:
        """
        Calculates final salary
        :return final_salary_value: Salary after taxes
        """
        (
            compulsory_social_health_insurance_value,
            compulsory_social_health_insurance_schema,
        ) = self.compulsory_health_insurance()
        social_deductions_value, social_deductions_schema = self.social_deductions()
        (
            social_contributions_value,
            social_contributions_schema,
        ) = self.social_contributions()
        health_insurance_value, health_insurance_schema = self.health_insurance()
        superannuation_value, superannuation_schema = self.superannuation()
        (
            personal_income_tax_value,
            personal_income_tax_schema,
        ) = self.personal_income_tax()

        final_salary_value = (
            self.salary
            - superannuation_value
            - personal_income_tax_value
            - health_insurance_value
        )

        schema = {
            "social_deductions": {
                "value": social_deductions_value,
                "schema": social_deductions_schema.as_dict(),
            },
            "compulsory_social_health_insurance": {
                "value": compulsory_social_health_insurance_value,
                "schema": compulsory_social_health_insurance_schema.as_dict(),
            },
            "social_contributions": {
                "value": social_contributions_value,
                "schema": social_contributions_schema.as_dict(),
            },
            "health_insurance": {
                "value": health_insurance_value,
                "schema": health_insurance_schema.as_dict(),
            },
            "superannuation": {
                "value": superannuation_value,
                "schema": superannuation_schema.as_dict(),
            },
            "personal_income_tax": {
                "value": personal_income_tax_value,
                "schema": personal_income_tax_schema.as_dict(),
            },
        }
        if not as_dict:  # pragma: no cover
            schema = {
                "social_deductions": {
                    "value": social_deductions_value,
                    "schema": social_deductions_schema,
                },
                "compulsory_social_health_insurance": {
                    "value": compulsory_social_health_insurance_value,
                    "schema": compulsory_social_health_insurance_schema,
                },
                "social_contributions": {
                    "value": social_contributions_value,
                    "schema": social_contributions_schema,
                },
                "health_insurance": {
                    "value": health_insurance_value,
                    "schema": health_insurance_schema,
                },
                "superannuation": {
                    "value": superannuation_value,
                    "schema": superannuation_schema,
                },
                "personal_income_tax": {
                    "value": personal_income_tax_value,
                    "schema": personal_income_tax_schema,
                },
            }

        return final_salary_value, schema
