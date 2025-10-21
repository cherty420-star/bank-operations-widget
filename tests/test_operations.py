import pytest

from src.operations import process_bank_operations, process_bank_search


class TestProcessBankSearch:
    def test_search_with_results(self):
        data = [
            {'description': 'Перевод организации', 'amount': 100},
            {'description': 'Открытие вклада', 'amount': 200},
            {'description': 'Перевод с карты на карту', 'amount': 300}
        ]
        result = process_bank_search(data, 'перевод')
        assert len(result) == 2


class TestProcessBankOperations:
    def test_count_operations(self):
        data = [
            {'description': 'Перевод организации'},
            {'description': 'Открытие вклада'},
            {'description': 'Перевод с карты на карту'}
        ]
        result = process_bank_operations(data, ['перевод', 'вклад'])
        assert result == {'перевод': 2, 'вклад': 1}