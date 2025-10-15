import pytest
import json
import tempfile
import os
import logging
from unittest.mock import patch
from src.utils.file_reader import read_transactions_from_json


class TestFileReader:

    def test_read_valid_json_file(self):
        """Тестирование чтения валидного JSON файла"""
        test_data = [
            {"id": 1, "amount": 100, "currency": "RUB"},
            {"id": 2, "amount": 50, "currency": "USD"}
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_path = f.name

        try:
            with patch.object(logging.getLogger('utils.file_reader'), 'info') as mock_info:
                result = read_transactions_from_json(temp_path)
                assert result == test_data
                mock_info.assert_called_once()
        finally:
            os.unlink(temp_path)

    def test_read_file_not_found(self):
        """Тестирование случая когда файл не существует"""
        with patch.object(logging.getLogger('utils.file_reader'), 'error') as mock_error:
            result = read_transactions_from_json("nonexistent_file.json")
            assert result == []
            mock_error.assert_called_once()