from hestia.bills.datatypes import (  # isort:skip
    Bill,
    BillItem,
    SalaryTaxCalculatorMixinBillsAlias,
    SalaryTaxSchema,
)


def test_bill():
    bill = Bill(title="1", bill="21")

    assert bill.title == "1"
    assert bill.bill == "21"
    assert bill.as_dict() == {"title": "1", "bill": "21"}


def test_bill_item():
    bill = Bill(title="1", bill="21")

    assert bill.title == "1"
    assert bill.bill == "21"
    assert bill.as_dict() == {"title": "1", "bill": "21"}

    bill_item = BillItem(topic="Topic", bills=[bill])

    assert bill_item.topic == "Topic"
    assert bill_item.bills == [bill]
    assert bill_item.as_dict() == {
        "topic": "Topic",
        "bills": [{"title": "1", "bill": "21"}],
    }


def test_salary_tax_schema():
    tax_schema = SalaryTaxSchema(debit=1, credit=2)

    assert tax_schema.debit == 1
    assert tax_schema.credit == 2
    assert tax_schema.as_dict() == {"debit": 1, "credit": 2}


def test_salary_tax_calculator_mixin_bills_alias():
    aliases = SalaryTaxCalculatorMixinBillsAlias()

    assert aliases
