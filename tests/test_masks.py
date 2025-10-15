import pytest
import logging
from unittest.mock import patch, Mock
from src.masks import get_mask_card_number, get_mask_account


class TestMasks:
    
    def test_get_mask_card_number_valid(self):
        """Тестирование маскировки валидного номера карты"""
        with patch.object(logging.getLogger('masks'), 'info') as mock_info:
            result = get_mask_card_number("1234567890123456")
            assert result == "1234 56** **** 3456"
            mock_info.assert_called_once()
    
    def test_get_mask_card_number_invalid(self):
        """Тестирование маскировки невалидного номера карты"""
        with patch.object(logging.getLogger('masks'), 'error') as mock_error:
            result = get_mask_card_number("123")
            assert result == "123"
            mock_error.assert_called_once()
    
    def test_get_mask_account_valid(self):
        """Тестирование маскировки валидного номера счета"""
        with patch.object(logging.getLogger('masks'), 'info') as mock_info:
            result = get_mask_account("12345678901234567890")
            assert result == "**7890"
            mock_info.assert_called_once()
    
    def test_get_mask_account_invalid(self):
        """Тестирование маскировки невалидного номера счета"""
        with patch.object(logging.getLogger('masks'), 'error') as mock_error:
            result = get_mask_account("123")
            assert result == "123"
            mock_error.assert_called_once()