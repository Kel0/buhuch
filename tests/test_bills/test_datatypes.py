from buhuch.bills.datatypes import Bill, BillItem


def test_bill():
    bill = Bill(title="1", bill="21")

    assert bill.title == "1"
    assert bill.bill == "21"


def test_bill_item():
    bill = Bill(title="1", bill="21")

    assert bill.title == "1"
    assert bill.bill == "21"

    bill_item = BillItem(topic="Topic", bills=[bill])

    assert bill_item.topic == "Topic"
    assert bill_item.bills == [bill]
