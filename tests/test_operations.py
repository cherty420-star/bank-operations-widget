import pytest
from src.operations import process_bank_search, process_bank_operations


class TestProcessBankSearch:
    def test_search_with_results(self):
        data = [
            {'description': 'Перевод организации', 'amount': 100},
            {'description': 'Открытие вклада', 'amount': 200},
            {'description': 'Перевод с карты на карту', 'amount': 300}
        ]
        result = process_bank_search(data, 'перевод')
        assert len(result) == 2

    def test_search_case_insensitive(self):
        data = [
            {'description': 'Перевод организации'},
            {'description': 'ПЕРЕВОД средств'},
            {'description': 'перевод денег'}
        ]
        result = process_bank_search(data, 'ПЕРЕВОД')
        assert len(result) == 3

    def test_search_no_results(self):
        data = [{'description': 'Открытие вклада'}]
        result = process_bank_search(data, 'перевод')
        assert result == []

    def test_empty_data(self):
        assert process_bank_search([], 'перевод') == []


class TestProcessBankOperations:
    def test_count_operations(self):
        data = [
            {'description': 'Перевод организации'},
            {'description': 'Открытие вклада'},
            {'description': 'Перевод с карты на карту'},
            {'description': 'Пополнение вклада'}
        ]
        result = process_bank_operations(data, ['перевод', 'вклад'])
        assert result == {'перевод': 2, 'вклад': 2}

    def test_count_case_insensitive(self):
        data = [
            {'description': 'ПЕРЕВОД организации'},
            {'description': 'перевод средств'},
            {'description': 'Открытие ВКЛАДА'}
        ]
        result = process_bank_operations(data, ['ПЕРЕВОД', 'вклад'])
        assert result == {'перевод': 2, 'вклад': 1}

    def test_count_no_matches(self):
        data = [{'description': 'Открытие вклада'}]
        result = process_bank_operations(data, ['перевод'])
        assert result == {'перевод': 0}

    def test_empty_data(self):
        assert process_bank_operations([], ['перевод']) == {}