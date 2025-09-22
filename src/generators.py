# src/generators.py
from typing import List, Dict, Any, Iterator, Generator


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по валюте и возвращает итератор.

    Args:
        transactions: Список транзакций
        currency: Код валюты для фильтрации (например, 'USD', 'RUB', 'EUR')

    Yields:
        Транзакции с указанной валютой
    """
    for transaction in transactions:
        if transaction.get('operationAmount', {}).get('currency', {}).get('code') == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """
    Генератор описаний транзакций.

    Args:
        transactions: Список транзакций

    Yields:
        Описание каждой транзакции
    """
    for transaction in transactions:
        yield transaction.get('description', '')


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    Генератор номеров банковских карт в заданном диапазоне.

    Args:
        start: Начальный номер (от 1)
        end: Конечный номер (до 9999999999999999)

    Yields:
        Номер карты в формате XXXX XXXX XXXX XXXX
    """
    for number in range(start, end + 1):
        # Форматируем номер с ведущими нулями
        card_number = str(number).zfill(16)
        # Разбиваем на группы по 4 цифры
        formatted_number = ' '.join([card_number[i:i + 4] for i in range(0, 16, 4)])
        yield formatted_number