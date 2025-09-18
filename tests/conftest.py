# tests/conftest.py (дополняем)
import pytest
from typing import List, Dict


@pytest.fixture
def sample_operations() -> List[Dict]:
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2024-03-15T10:30:00.000000', 'amount': 100},
        {'id': 2, 'state': 'PENDING', 'date': '2024-03-14T12:15:00.000000', 'amount': 200},
        {'id': 3, 'state': 'EXECUTED', 'date': '2024-03-16T08:45:00.000000', 'amount': 300},
        {'id': 4, 'state': 'CANCELED', 'date': '2024-03-13T16:20:00.000000', 'amount': 400}
    ]


@pytest.fixture
def account_data() -> List[str]:
    return [
        "Visa Platinum 7000792289606361",
        "Счет 73654108430135874305",
        "Maestro 1596837868705199",
        "Visa Classic 1234567890123456",
        "Счет 12345678901234567890"
    ]


@pytest.fixture
def date_data() -> List[str]:
    return [
        "2024-03-11T02:26:18.671407",
        "2023-12-31T23:59:59.999999",
        "2023-01-01T00:00:00.000000",
        "2022-02-28T15:30:45.123456"
    ]