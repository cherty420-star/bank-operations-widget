"""
Модуль для конвертации валют.
"""

from typing import Dict, Optional, Union


class CurrencyConverter:
    """
    Упрощенный конвертер валют для демонстрационных целей.
    """

    def __init__(self) -> None:
        """Инициализация конвертера валют."""
        # Фиксированные курсы для демонстрации
        self.exchange_rates: Dict[str, Dict[str, float]] = {
            'USD': {'RUB': 90.0, 'EUR': 0.85},
            'EUR': {'USD': 1.18, 'RUB': 95.0},
            'RUB': {'USD': 0.011, 'EUR': 0.0105}
        }

    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> Optional[float]:
        """
        Конвертирует сумму из одной валюты в другую.

        Args:
            amount: Сумма для конвертации
            from_currency: Исходная валюта
            to_currency: Целевая валюта

        Returns:
            Optional[float]: Конвертированная сумма или None при ошибке
        """
        if from_currency == to_currency:
            return amount

        if from_currency not in self.exchange_rates:
            print(f"Валюта {from_currency} не поддерживается")
            return None

        if to_currency not in self.exchange_rates[from_currency]:
            print(f"Конвертация из {from_currency} в {to_currency} не поддерживается")
            return None

        rate = self.exchange_rates[from_currency][to_currency]
        converted_amount: float = amount * rate
        return converted_amount


def main() -> None:
    """Демонстрация работы конвертера валют."""
    converter = CurrencyConverter()

    # Примеры конвертации
    test_cases = [
        (100, "USD", "RUB"),
        (50, "EUR", "USD"),
        (1000, "RUB", "EUR")
    ]

    print("Демонстрация конвертера валют:")
    for amount, from_curr, to_curr in test_cases:
        result = converter.convert_currency(amount, from_curr, to_curr)
        if result is not None:
            print(f"{amount} {from_curr} = {result:.2f} {to_curr}")
        else:
            print(f"Не удалось конвертировать {amount} {from_curr} в {to_curr}")


if __name__ == "__main__":
    main()