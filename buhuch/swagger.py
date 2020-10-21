from datetime import datetime

from .utils import scrape_min_salary


class SalaryTaxCalculatorMixin:
    def __init__(
        self,
        salary: float = 0,
        year: int = datetime.now().year,
    ) -> None:
        self.salary = salary
        self.min_salary = scrape_min_salary(year)

    def superannuation(self) -> float:
        """
        Superannuation calculation formula:
            salary * 10%
        :return superannuation: Superannuation value
        """
        superannuation = self.salary * 0.1
        return superannuation

    def corrections_salary_superannuation_min_salary(self) -> float:
        """
        Salary corrections calculation formula:
            (salary - superannuation - min_salary) * 90%
        :return corrections_value: Correction value
        """
        corrections_value = (
            self.salary - self.superannuation() - self.min_salary
        ) * 0.9
        return corrections_value

    def personal_income_tax(self) -> float:
        """
        Personal income tax calculation formula:
            (salary - superannuation - min_salary - corrections_salary_superannuation_min_salary) * 10%
        :return income_value: Income tax value
        """
        income_value = (
            self.salary
            - self.superannuation()
            - self.min_salary
            - self.corrections_salary_superannuation_min_salary()
        ) * 0.1
        return income_value

    def health_insurance(self) -> float:
        """
        Formula for calculate health insurance tax formula:
            (salary * 0.01)
        :return health_insurance_value: Price of health insurance
        """
        health_insurance_value = self.salary * 0.01
        return health_insurance_value

    def social_contributions(self) -> float:
        """
        Formula for calculate social contributions tax formula:
            (salary - superannuation) * 0.035
        :return social_contributions_value: Price of health insurance
        """
        social_contributions_value = (self.salary - self.superannuation()) * 0.035
        return social_contributions_value

    def social_receives(self) -> float:
        """
        Formula for calculate social receives formula:
            (salary - superannuation - health_insurance) * 0.095 - social_contributions
        :return social_receives_value: Social receives value
        """
        social_receives_value = (
            self.salary - self.superannuation() - self.health_insurance()
        ) * 0.095 - self.social_contributions()
        return social_receives_value

    def compulsory_social_health_insurance(self) -> float:
        """
        Formula for calculate compulsory social health insurance formula:
            (salary * 0.02)
        :return compulsory_social_health_insurance_value: Compulsory social health insurance value
        """
        compulsory_social_health_insurance_value = self.salary * 0.02
        return compulsory_social_health_insurance_value
