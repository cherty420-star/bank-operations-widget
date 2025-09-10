from datetime import datetime
from typing import List, Dict, Any, Optional


def filter_by_state(operations: List[Dict[str, Any]],
                    state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """
    Фильтрует список операций по статусу.

    Args:
        operations: список словарей с операциями
        state: статус для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        List[Dict]: отфильтрованный список операций
    """
    return [op for op in operations if op.get('state') == state]


def sort_by_date(operations: List[Dict[str, Any]],
                 reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список операций по дате.

    Args:
        operations: список словарей с операциями
        reverse: порядок сортировки (True - по убыванию, False - по возрастанию)

    Returns:
        List[Dict]: отсортированный список операций
    """

    def get_date(op: Dict[str, Any]) -> datetime:
        date_str = op.get('date', '')
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except ValueError:
            return datetime.min

    return sorted(operations, key=get_date, reverse=reverse)