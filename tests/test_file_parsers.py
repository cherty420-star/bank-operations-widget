import sys
import os
# Добавляем корневую директорию в Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, mock_open
import pandas as pd

from file_parsers import read_csv_transactions, read_excel_transactions

class TestFileParsers:
    """Тесты для модуля парсинга файлов"""

    @patch('pandas.read_csv')
    def test_read_csv_transactions_success(self, mock_read_csv):
        """Тест успешного чтения CSV-файла"""
        # Arrange
        mock_data = pd.DataFrame([
            {'id': 1, 'amount': 100, 'date': '2023-01-01'},
            {'id': 2, 'amount': 200, 'date': '2023-01-02'}
        ])
        mock_read_csv.return_value = mock_data

        # Act
        result = read_csv_transactions('test.csv')

        # Assert
        assert len(result) == 2
        assert result[0]['id'] == 1
        assert result[1]['amount'] == 200
        mock_read_csv.assert_called_once_with('test.csv')

    @patch('pandas.read_csv')
    def test_read_csv_transactions_empty_file(self, mock_read_csv):
        """Тест чтения пустого CSV-файла"""
        # Arrange
        mock_read_csv.side_effect = pd.errors.EmptyDataError("No columns to parse")

        # Act
        result = read_csv_transactions('empty.csv')

        # Assert
        assert result == []

    @patch('pandas.read_csv')
    def test_read_csv_transactions_file_not_found(self, mock_read_csv):
        """Тест обработки отсутствующего CSV-файла"""
        # Arrange
        mock_read_csv.side_effect = FileNotFoundError("File not found")

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            read_csv_transactions('nonexistent.csv')

    @patch('pandas.read_excel')
    def test_read_excel_transactions_success(self, mock_read_excel):
        """Тест успешного чтения Excel-файла"""
        # Arrange
        mock_data = pd.DataFrame([
            {'id': 1, 'amount': 150, 'date': '2023-01-01', 'description': 'Payment'},
            {'id': 2, 'amount': -50, 'date': '2023-01-02', 'description': 'Withdrawal'}
        ])
        mock_read_excel.return_value = mock_data

        # Act
        result = read_excel_transactions('test.xlsx')

        # Assert
        assert len(result) == 2
        assert result[0]['description'] == 'Payment'
        assert result[1]['amount'] == -50
        mock_read_excel.assert_called_once_with('test.xlsx')

    @patch('pandas.read_excel')
    def test_read_excel_transactions_file_not_found(self, mock_read_excel):
        """Тест обработки отсутствующего Excel-файла"""
        # Arrange
        mock_read_excel.side_effect = FileNotFoundError("File not found")

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            read_excel_transactions('nonexistent.xlsx')


def test_csv_transactions_integration():
    """Интеграционный тест для CSV (требует наличия тестового файла)"""
    try:
        transactions = read_csv_transactions('transactions.csv')
        assert isinstance(transactions, list)
        if transactions:
            assert isinstance(transactions[0], dict)
    except FileNotFoundError:
        pytest.skip("Тестовый CSV-файл не найден")


def test_excel_transactions_integration():
    """Интеграционный тест для Excel (требует наличия тестового файла)"""
    try:
        transactions = read_excel_transactions('transactions_excel.xlsx')
        assert isinstance(transactions, list)
        if transactions:
            assert isinstance(transactions[0], dict)
    except FileNotFoundError:
        pytest.skip("Тестовый Excel-файл не найден")

