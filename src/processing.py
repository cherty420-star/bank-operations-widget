# Создадим файл processing.py в папке src
echo "from typing import List, Dict, Any
from datetime import datetime


def filter_by_state(operations: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    '''Фильтрует операции по статусу.'''
    return [op for op in operations if op.get('state') == state]


def sort_by_date(operations: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    '''Сортирует операции по дате.'''
    def get_date(op: Dict[str, Any]) -> datetime:
        date_str = op.get('date', '')
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except ValueError:
            return datetime.min

    return sorted(operations, key=get_date, reverse=reverse)" > src/processing.py