import pytest
from unittest.mock import patch, Mock
from src.external_api.currency_converter import CurrencyConverter, get_transaction_amount_in_rubles


class TestCurrencyConverter:

    @patch('src.external_api.currency_converter.requests.get')
    def test_get_exchange_rate_success(self, mock_get):
        """Тестирование успешного получения курса валют"""
        # Мокаем ответ API
        mock_response = Mock()
        mock_response.json.return_value = {
            'rates': {'RUB': 90.5},
            'base': 'USD',
            'success': True
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Сначала мокаем переменные окружения, потом создаем экземпляр
        with patch.dict('os.environ', {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            converter = CurrencyConverter()  # Создаем после мока!
            rate = converter.get_exchange_rate('USD', 'RUB')

        assert rate == 90.5
        mock_get.assert_called_once()

    @patch('src.external_api.currency_converter.requests.get')
    def test_get_exchange_rate_failure(self, mock_get):
        """Тестирование ошибки при получении курса"""
        mock_get.side_effect = ConnectionError("API unavailable")

        # Сначала мокаем переменные окружения
        with patch.dict('os.environ', {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            converter = CurrencyConverter()  # Создаем после мока!
            with pytest.raises(ConnectionError):
                converter.get_exchange_rate('USD', 'RUB')

    def test_convert_rubles_no_conversion(self):
        """Тестирование конвертации RUB (без конвертации)"""
        transaction = {'amount': '100.0', 'currency': 'RUB'}

        with patch.dict('os.environ', {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            converter = CurrencyConverter()
            result = converter.convert_to_rubles(transaction)

        assert result == 100.0

    @patch('src.external_api.currency_converter.CurrencyConverter.get_exchange_rate')
    def test_convert_usd_to_rubles(self, mock_rate):
        """Тестирование конвертации USD в RUB"""
        mock_rate.return_value = 90.5
        transaction = {'amount': '10.0', 'currency': 'USD'}

        with patch.dict('os.environ', {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            converter = CurrencyConverter()
            result = converter.convert_to_rubles(transaction)

        assert result == 905.0  # 10 * 90.5
        mock_rate.assert_called_once_with('USD', 'RUB')

    def test_convert_unknown_currency(self):
        """Тестирование конвертации неизвестной валюты"""
        transaction = {'amount': '50.0', 'currency': 'GBP'}

        with patch.dict('os.environ', {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            converter = CurrencyConverter()
            result = converter.convert_to_rubles(transaction)

        assert result == 50.0

    def test_get_transaction_amount_function(self):
        """Тестирование функции-обертки"""
        transaction = {'amount': '100.0', 'currency': 'RUB'}

        with patch('src.external_api.currency_converter.CurrencyConverter.convert_to_rubles') as mock_convert:
            mock_convert.return_value = 100.0
            result = get_transaction_amount_in_rubles(transaction)

        assert result == 100.0
        mock_convert.assert_called_once_with(transaction)

    def test_missing_api_key(self):
        """Тестирование случая когда API ключ отсутствует"""
        # Убедимся что переменная окружения не установлена
        with patch.dict('os.environ', {}, clear=True):
            converter = CurrencyConverter()
            with pytest.raises(ValueError, match="API key not found"):
                converter.get_exchange_rate('USD', 'RUB')