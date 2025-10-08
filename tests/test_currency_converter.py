import pytest
from unittest.mock import patch, Mock
from src.external_api.currency_converter import CurrencyConverter, get_transaction_amount_in_rubles


class TestCurrencyConverter:

    @patch('src.external_api.currency_converter.requests.get')
    def test_get_exchange_rate_success(self, mock_get):
        """Тестирование успешного получения курса валют"""
        # Мокаем ответ API для endpoint /convert
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': True,
            'result': 90.5,
            'query': {'from': 'USD', 'to': 'RUB', 'amount': 1}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with patch.dict('os.environ', {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            converter = CurrencyConverter()
            rate = converter.get_exchange_rate('USD', 'RUB')

        assert rate == 90.5
        # Проверяем что URL правильный для /convert
        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=1",
            headers={'apikey': 'test_key'},
            timeout=10
        )

    @patch('src.external_api.currency_converter.requests.get')
    def test_get_exchange_rate_api_error(self, mock_get):
        """Тестирование ошибки API"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': False,
            'error': {'info': 'Invalid API key'}
        }
        mock_get.return_value = mock_response

        with patch.dict('os.environ', {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            converter = CurrencyConverter()
            with pytest.raises(ValueError, match="API error"):
                converter.get_exchange_rate('USD', 'RUB')

    @patch('src.external_api.currency_converter.requests.get')
    def test_get_exchange_rate_no_result(self, mock_get):
        """Тестирование ответа без результата"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': True,
            # Нет поля 'result'
        }
        mock_get.return_value = mock_response

        with patch.dict('os.environ', {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            converter = CurrencyConverter()
            with pytest.raises(ValueError, match="Result not found"):
                converter.get_exchange_rate('USD', 'RUB')

    # Остальные тесты остаются без изменений...
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