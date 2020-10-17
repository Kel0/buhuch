import dataclasses
import json

import pytest


class Helpers:
    def read_json(self, filename: str):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    def txt_to_bytes(self, filename: str):
        with open(filename, "r") as f:
            data = f.read()
        return data.encode()

    def bills_list_to_dict(self, bills):
        bills_json = []
        for bill in bills:
            bills_json.append(dataclasses.asdict(bill))

        return bills_json


@pytest.fixture
def helpers():
    return Helpers()
