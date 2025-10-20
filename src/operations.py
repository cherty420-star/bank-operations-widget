import re
from collections import Counter
from typing import List, Dict, Any


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Ищет операции по заданной строке в описании с использованием регулярных выражений.
    """
    if not data or not search:
        return []

    result: List[Dict[str, Any]] = []
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    for operation in data:
        description = operation.get('description', '')
        if description and pattern.search(description):
            result.append(operation)

    return result


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по заданным категориям.
    """
    if not data or not categories:
        return {}

    categories_lower = [category.lower() for category in categories]
    # Добавляем аннотацию типа для category_counter
    category_counter: Counter[str] = Counter()

    for operation in data:
        description = operation.get('description', '').lower()
        if description:
            for category in categories_lower:
                if category in description:
                    category_counter[category] += 1

    return dict(category_counter)