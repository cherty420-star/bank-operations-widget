import json
import csv
import pandas as pd
from typing import List, Dict, Any


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON файл с операциями.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return data.get('operations', [])
        return []
    except Exception as e:
        print(f"Ошибка чтения JSON файла: {e}")
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
                # Конвертируем типы данных
                operation = {
                    'id': int(row.get('id', 0)),
                    'state': row.get('state', ''),
                    'date': row.get('date', ''),
                    'amount': float(row.get('amount', 0)),
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
        operations = df.to_dict('records')
        return operations
    except Exception as e:
        print(f"Ошибка чтения Excel файла: {e}")
        return []