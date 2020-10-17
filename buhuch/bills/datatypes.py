"""
Bills datatypes
~~~~~~~~~~~~~~~

This module provides "Bill" typed entities
"""
from dataclasses import dataclass
from typing import List


@dataclass
class Bill:
    title: str
    bill: str


@dataclass
class BillItem:
    topic: str
    bills: List[Bill]


BillsList = List[BillItem]
