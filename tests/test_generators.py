# tests/test_generators.py
import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions():
    return [
        {
            'id': 1,
            'description': 'Перевод организации',
            'operationAmount': {'amount': '100.00', 'currency': {'code': 'USD', 'name': 'US Dollar'}}
        },
        {
            'id': 2,
            'description': 'Перевод со счета на счет',
            'operationAmount': {'amount': '200.00', 'currency': {'code': 'RUB', 'name': 'Russian Ruble'}}
        },
        {
            'id': 3,
            'description': 'Перевод с карты на карту',
            'operationAmount': {'amount': '300.00', 'currency': {'code': 'USD', 'name': 'US Dollar'}}
        },
        {
            'id': 4,
            'description': 'Оплата услуг',
            'operationAmount': {'amount': '400.00', 'currency': {'code': 'EUR', 'name': 'Euro'}}
        }
    ]


class TestGenerators:
    def test_filter_by_currency(self, sample_transactions):
        """Тестирование фильтрации транзакций по валюте"""
        usd_transactions = list(filter_by_currency(sample_transactions, 'USD'))
        assert len(usd_transactions) == 2
        assert all(t['operationAmount']['currency']['code'] == 'USD' for t in usd_transactions)
        assert usd_transactions[0]['id'] == 1
        assert usd_transactions[1]['id'] == 3

    def test_filter_by_currency_empty(self, sample_transactions):
        """Тестирование фильтрации при отсутствии валюты"""
        gbp_transactions = list(filter_by_currency(sample_transactions, 'GBP'))
        assert len(gbp_transactions) == 0

    def test_transaction_descriptions(self, sample_transactions):
        """Тестирование генератора описаний транзакций"""
        descriptions = list(transaction_descriptions(sample_transactions))
        expected_descriptions = [
            'Перевод организации',
            'Перевод со счета на счет',
            'Перевод с карты на карту',
            'Оплата услуг'
        ]
        assert descriptions == expected_descriptions

    @pytest.mark.parametrize('start, end, expected_count, first_number, last_number', [
        (1, 5, 5, '0000 0000 0000 0001', '0000 0000 0000 0005'),
        (9999999999999995, 9999999999999999, 5, '9999 9999 9999 9995', '9999 9999 9999 9999'),
        (1234567890123456, 1234567890123456, 1, '1234 5678 9012 3456', '1234 5678 9012 3456'),
    ])
    def test_card_number_generator(self, start, end, expected_count, first_number, last_number):
        """Тестирование генератора номеров карт с параметризацией"""
        numbers = list(card_number_generator(start, end))
        assert len(numbers) == expected_count
        assert numbers[0] == first_number
        assert numbers[-1] == last_number
        # Проверяем формат всех номеров
        for number in numbers:
            assert len(number) == 19  # XXXX XXXX XXXX XXXX
            assert number.count(' ') == 3
            assert number.replace(' ', '').isdigit()

    def test_card_number_generator_small_range(self):
        """Тестирование генератора для маленького диапазона"""
        numbers = list(card_number_generator(1, 3))
        assert numbers == ['0000 0000 0000 0001', '0000 0000 0000 0002', '0000 0000 0000 0003']