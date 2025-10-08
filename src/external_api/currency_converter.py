import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


class CurrencyConverter:
    def __init__(self):
        self.api_key = os.getenv('EXCHANGE_RATE_API_KEY')
        self.base_url = "https://api.apilayer.com/exchangerates_data"

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

        # ПРАВИЛЬНЫЙ URL согласно документации API
        url = f"{self.base_url}/convert?to={to_currency}&from={from_currency}&amount=1"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Проверяем структуру ответа для endpoint /convert
            if not data.get('success', True):
                error_info = data.get('error', {})
                raise ValueError(f"API error: {error_info.get('info', 'Unknown error')}")

            # Для endpoint /convert результат в поле 'result'
            result = data.get('result')
            if result is None:
                raise ValueError("Result not found in API response")

            return float(result)

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to fetch exchange rate: {e}")
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Invalid response format: {e}")

    def convert_to_rubles(self, transaction: Dict[str, Any]) -> float:
        """
        Конвертирует сумму транзакции в рубли.

        Args:
            transaction: Словарь с данными транзакции

        Returns:
            Сумма в рублях (float)
        """
        try:
            amount = float(transaction.get('amount', 0))
            currency = transaction.get('currency', 'RUB')

            # Если уже в рублях, возвращаем как есть
            if currency == 'RUB':
                return amount

            # Если в поддерживаемой валюте, конвертируем
            if currency in ['USD', 'EUR']:
                rate = self.get_exchange_rate(currency, 'RUB')
                return amount * rate

            # Для неизвестных валют возвращаем как есть
            return amount

        except (ValueError, TypeError):
            # Если amount нельзя преобразовать в float
            return 0.0


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