import pytest
import json
import tempfile
import os
from src.utils.file_reader import read_transactions_from_json


class TestFileReader:
    def test_read_valid_json_file(self):
        """Тестирование чтения валидного JSON файла"""
        # Создаем временный файл с данными
        test_data = [
            {"id": 1, "amount": 100, "currency": "RUB"},
            {"id": 2, "amount": 50, "currency": "USD"}
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_path = f.name

        try:
            result = read_transactions_from_json(temp_path)
            assert result == test_data
        finally:
            os.unlink(temp_path)

    def test_read_empty_file(self):
        """Тестирование чтения пустого файла"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("")
            temp_path = f.name

        try:
            result = read_transactions_from_json(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_read_invalid_json(self):
        """Тестирование чтения невалидного JSON"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content")
            temp_path = f.name

        try:
            result = read_transactions_from_json(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_read_non_list_json(self):
        """Тестирование чтения JSON не в формате списка"""
        test_data = {"id": 1, "amount": 100}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_path = f.name

        try:
            result = read_transactions_from_json(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_file_not_found(self):
        """Тестирование случая когда файл не существует"""
        result = read_transactions_from_json("nonexistent_file.json")
        assert result == []