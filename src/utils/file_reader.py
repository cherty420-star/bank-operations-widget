import csv
import json
import os
from typing import Any, Dict, List

import pandas as pd


def read_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает транзакции из JSON-файла.
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            return []

        # Читаем файл
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем что данные - список
        if isinstance(data, list):
            return data
        else:
            return []

    except (json.JSONDecodeError, IOError):
        # Если файл пустой, поврежден или ошибка чтения
        return []


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает CSV файл с операциями.
    """
    try:
        operations = []
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Создаем операцию с правильными типами данных
                operation = {
                    'id': int(row['id']) if row.get('id') and row['id'].strip().isdigit() else 0,
                    'state': row.get('state', ''),
                    'date': row.get('date', ''),
                    'amount': float(row['amount']) if row.get('amount') and row['amount'].strip() else 0.0,
                    'currency': row.get('currency', 'RUB'),
                    'description': row.get('description', ''),
                    'from': row.get('from', ''),
                    'to': row.get('to', '')
                }
                operations.append(operation)
        return operations
    except Exception as e:
        print(f"Ошибка чтения CSV файла: {e}")
        return []


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает Excel файл с операциями.
    """
    try:
        df = pd.read_excel(file_path)
        # Заменяем NaN значения на пустые строки
        df = df.fillna('')
        operations = df.to_dict('records')

        # Обрабатываем типы данных
        for operation in operations:
            # Преобразуем числовые поля в строки где нужно
            if 'from' in operation:
                operation['from'] = str(operation['from']) if operation['from'] else ''
            if 'to' in operation:
                operation['to'] = str(operation['to']) if operation['to'] else ''

        return operations
    except Exception as e:
        print(f"Ошибка чтения Excel файла: {e}")
        return []