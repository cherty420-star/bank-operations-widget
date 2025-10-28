from collections import Counter
import re
from typing import Any, Dict, List


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Ищет операции по заданной строке в описании с использованием регулярных выражений.
    """
    if not data or not search:
        return []

    result = []
    # Используем полноценное регулярное выражение для поиска слов
    pattern = re.compile(r'\b' + re.escape(search) + r'\b', re.IGNORECASE)

    for operation in data:
        description = operation.get('description', '')
        if description and pattern.search(description):
            result.append(operation)

    return result


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по заданным категориям с использованием Counter.
    """
    if not data or not categories:
        return {}

    categories_lower = [category.lower() for category in categories]
    category_counter = Counter()

    for operation in data:
        description = operation.get('description', '').lower()
        if description:
            # Ищем все категории, которые встречаются в описании
            found_categories = [cat for cat in categories_lower if cat in description]
            category_counter.update(found_categories)

    # Преобразуем Counter в обычный dict и добавляем отсутствующие категории
    result = dict(category_counter)
    for category in categories_lower:
        if category not in result:
            result[category] = 0

    return result