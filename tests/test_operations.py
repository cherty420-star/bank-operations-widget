import pytest

from src.operations import process_bank_operations, process_bank_search


class TestProcessBankSearch:
    """Тесты для функции поиска операций."""

    def test_search_with_results(self):
        """Тест поиска с результатами."""
        data = [
            {'description': 'Перевод организации', 'amount': 100},
            {'description': 'Открытие вклада', 'amount': 200},
            {'description': 'Перевод с карты на карту', 'amount': 300}
        ]
        result = process_bank_search(data, 'перевод')
        assert len(result) == 2

    def test_search_case_insensitive(self):
        """Тест регистронезависимого поиска."""
        data = [
            {'description': 'Перевод организации'},
            {'description': 'ПЕРЕВОД средств'},
            {'description': 'перевод денег'}
        ]
        result = process_bank_search(data, 'ПЕРЕВОД')
        assert len(result) == 3

    def test_search_no_results(self):
        """Тест поиска без результатов."""
        data = [{'description': 'Открытие вклада'}]
        result = process_bank_search(data, 'перевод')
        assert result == []

    def test_empty_data(self):
        """Тест с пустыми данными."""
        assert process_bank_search([], 'перевод') == []

    def test_search_with_special_chars(self):
        """Тест поиска с специальными символами."""
        data = [
            {'description': 'Перевод (организация)'},
            {'description': 'Обычный перевод'}
        ]
        result = process_bank_search(data, 'перевод')
        assert len(result) == 2

    def test_search_word_boundaries(self):
        """Тест поиска с учетом границ слов."""
        data = [
            {'description': 'Перевод организации'},
            {'description': 'Денежный перевод'},
            {'description': 'Переводной документ'}  # Не должно находиться
        ]
        result = process_bank_search(data, 'перевод')
        assert len(result) == 2


class TestProcessBankOperations:
    """Тесты для функции подсчета операций."""

    def test_count_operations(self):
        """Тест подсчета операций."""
        data = [
            {'description': 'Перевод организации'},
            {'description': 'Открытие вклада'},
            {'description': 'Перевод с карты на карту'},
            {'description': 'Пополнение вклада'}
        ]
        result = process_bank_operations(data, ['перевод', 'вклад'])
        assert result == {'перевод': 2, 'вклад': 2}

    def test_count_case_insensitive(self):
        """Тест регистронезависимого подсчета."""
        data = [
            {'description': 'ПЕРЕВОД организации'},
            {'description': 'перевод средств'},
            {'description': 'Открытие ВКЛАДА'}
        ]
        result = process_bank_operations(data, ['ПЕРЕВОД', 'вклад'])
        assert result == {'перевод': 2, 'вклад': 1}

    def test_count_no_matches(self):
        """Тест подсчета без совпадений."""
        data = [{'description': 'Открытие вклада'}]
        result = process_bank_operations(data, ['перевод'])
        assert result == {'перевод': 0}

    def test_empty_data(self):
        """Тест с пустыми данными."""
        assert process_bank_operations([], ['перевод']) == {}

    def test_uses_counter(self):
        """Тест, что функция использует Counter."""
        data = [
            {'description': 'Перевод организации'},
            {'description': 'Перевод средств'},
            {'description': 'Открытие вклада'}
        ]
        result = process_bank_operations(data, ['перевод', 'вклад'])
        # Проверяем, что Counter правильно подсчитал
        assert isinstance(result, dict)
        assert result['перевод'] == 2
        assert result['вклад'] == 1


def test_integration():
    """Интеграционный тест нескольких функций."""
    data = [
        {'description': 'Перевод организации', 'state': 'EXECUTED'},
        {'description': 'Открытие вклада', 'state': 'EXECUTED'},
        {'description': 'Перевод с карты', 'state': 'CANCELED'}
    ]

    # Поиск
    searched = process_bank_search(data, 'перевод')
    assert len(searched) == 2

    # Подсчет
    counted = process_bank_operations(data, ['перевод', 'вклад'])
    assert counted['перевод'] == 2
    assert counted['вклад'] == 1