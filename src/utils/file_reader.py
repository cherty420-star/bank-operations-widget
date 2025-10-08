import json
import os
from typing import List, Dict, Any


def read_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает транзакции из JSON-файла.

    Args:
        file_path: Путь до JSON-файла

    Returns:
        Список словарей с данными транзакций
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