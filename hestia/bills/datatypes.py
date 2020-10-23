"""
Bills data types
~~~~~~~~~~~~~~~~

This module provides "Bill" typed entities
"""
from dataclasses import dataclass
from typing import Dict, List, Union


@dataclass
class Bill:
    title: str
    bill: str

    def as_dict(self) -> Dict[str, str]:
        return {"title": self.title, "bill": self.bill}


@dataclass
class BillItem:
    topic: str
    bills: List[Bill]

    def as_dict(self) -> Dict[str, Union[str, List[Dict[str, str]]]]:
        return {"topic": self.topic, "bills": [bill.as_dict() for bill in self.bills]}


@dataclass
class SalaryTaxSchema:
    debit: int
    credit: int

    def as_dict(self) -> Dict[str, int]:
        return {"debit": self.debit, "credit": self.credit}


@dataclass(frozen=True)
class SalaryTaxCalculatorMixinBillsAlias:
    salary: SalaryTaxSchema = SalaryTaxSchema(debit=7210, credit=3350)
    superannuation: SalaryTaxSchema = SalaryTaxSchema(debit=3350, credit=3220)
    personal_income_tax: SalaryTaxSchema = SalaryTaxSchema(debit=3850, credit=3350)
    health_insurance: SalaryTaxSchema = SalaryTaxSchema(debit=3350, credit=3240)
    social_contributions: SalaryTaxSchema = SalaryTaxSchema(debit=7210, credit=3150)
    social_deductions: SalaryTaxSchema = SalaryTaxSchema(debit=7210, credit=3240)
    compulsory_health_insurance_value: SalaryTaxSchema = SalaryTaxSchema(
        debit=7210, credit=3240
    )


BillsList = List[BillItem]
