import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


class CurrencyConverter:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('EXCHANGE_RATE_API_KEY')
        self.base_url = "https://api.apilayer.com/exchangerates_data/latest"

    def get_exchange_rate(self, from_currency: str, to_currency: str = "RUB") -> float:
        """
        Получает текущий курс валюты.

        Args:
            from_currency: Исходная валюта (USD, EUR)
            to_currency: Целевая валюта (по умолчанию RUB)

        Returns:
            Курс обмена
        """
        if not self.api_key:
            raise ValueError("API key not found in environment variables")

        headers = {"apikey": self.api_key}
        params = {"base": from_currency, "symbols": to_currency}

        try:
            response = requests.get(self.base_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            return data['rates'][to_currency]

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to fetch exchange rate: {e}")
        except (KeyError, ValueError) as e:
            raise ValueError(f"Invalid response format: {e}")

    def convert_to_rubles(self, transaction: Dict[str, Any]) -> float:
        """
        Конвертирует сумму транзакции в рубли.

        Args:
            transaction: Словарь с данными транзакции

        Returns:
            Сумма в рублях (float)
        """
        amount = transaction.get('amount', 0)
        currency = transaction.get('currency', 'RUB')

        # Если уже в рублях, возвращаем как есть
        if currency == 'RUB':
            return float(amount)

        # Если в поддерживаемой валюте, конвертируем
        if currency in ['USD', 'EUR']:
            try:
                rate = self.get_exchange_rate(currency, 'RUB')
                return float(amount) * rate
            except Exception as e:
                # В случае ошибки API возвращаем исходную сумму
                print(f"Conversion error: {e}")
                return float(amount)

        # Для неизвестных валют возвращаем как есть
        return float(amount)


# Функция для удобного использования
def get_transaction_amount_in_rubles(transaction: Dict[str, Any]) -> float:
    """
    Возвращает сумму транзакции в рублях.

    Args:
        transaction: Словарь с данными транзакции

    Returns:
        Сумма в рублях
    """
    converter = CurrencyConverter()
    return converter.convert_to_rubles(transaction)