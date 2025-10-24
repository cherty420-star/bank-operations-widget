import re
from collections import Counter
from typing import List, Dict, Any


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Ищет операции по заданной строке в описании с использованием регулярных выражений.

    Args:
        data: Список словарей с данными о банковских операциях
        search: Строка для поиска в описании операций

    Returns:
        List[Dict]: Список операций, у которых в описании есть искомая строка
    """
    if not data or not search:
        return []

    result = []
    # Создаем case-insensitive паттерн для поиска
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    for operation in data:
        description = operation.get('description', '')
        if description and pattern.search(description):
            result.append(operation)

    return result


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по заданным категориям.

    Args:
        data: Список словарей с данными о банковских операциях
        categories: Список категорий для подсчета

    Returns:
        Dict[str, int]: Словарь с количеством операций по категориям
    """
    if not data or not categories:
        return {}

    # Приводим категории к нижнему регистру для case-insensitive сравнения
    categories_lower = [category.lower() for category in categories]

    # Используем Counter для эффективного подсчета
    category_counter = Counter()

    # Инициализируем счетчик нулями для всех категорий
    for category in categories_lower:
        category_counter[category] = 0

    for operation in data:
        description = operation.get('description', '').lower()
        if description:
            for category in categories_lower:
                if category in description:
                    category_counter[category] += 1

    return dict(category_counter)
