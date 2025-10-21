from typing import List, Dict, Any
import os
import json
from widget import mask_account_card, get_date
from operations import process_bank_search


def load_operations_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает операции из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу

    Returns:
        List[Dict]: Список операций
    """
    try:
        # Если путь не абсолютный, ищем файл в папке data
        if not os.path.isabs(file_path):
            data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
            file_path = os.path.join(data_dir, file_path)

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Если данные - список, возвращаем как есть
        if isinstance(data, list):
            return data
        # Если данные - словарь с ключом 'operations', извлекаем его
        elif isinstance(data, dict) and 'operations' in data:
            return data['operations']
        else:
            print("Неверный формат данных в JSON-файле")
            return []

    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка чтения JSON из файла {file_path}")
        return []
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return []


def load_operations(file_type: str) -> List[Dict[str, Any]]:
    """
    Загружает операции в зависимости от выбранного типа файла.

    Args:
        file_type: Тип файла ('1', '2', '3')

    Returns:
        List[Dict]: Список операций
    """
    if file_type == "1":  # JSON
        file_name = input("Введите имя JSON-файла (например: operations.json): ").strip()
        if not file_name:
            file_name = "operations.json"  # файл по умолчанию

        operations = load_operations_from_json(file_name)

        if operations:
            print(f"Успешно загружено {len(operations)} операций")
        else:
            print("Не удалось загрузить операции из файла")

        return operations

    elif file_type == "2":  # CSV
        print("Загрузка из CSV файлов будет реализована в будущем")
        return []

    elif file_type == "3":  # XLSX
        print("Загрузка из XLSX файлов будет реализована в будущем")
        return []

    return []


def format_operation(operation: Dict[str, Any]) -> str:
    """
    Форматирует операцию для красивого вывода.

    Args:
        operation: Данные операции

    Returns:
        str: Отформатированная строка с операцией
    """
    # Форматирование даты
    date = get_date(operation.get('date', ''))

    # Форматирование описания
    description = operation.get('description', 'Неизвестная операция')

    # Форматирование суммы и валюты
    amount = operation.get('amount', 0)
    currency = operation.get('currency', 'RUB')

    # Форматирование счета/карты (упрощенная версия)
    from_account = mask_account_card(operation.get('from', 'Неизвестно'))
    to_account = mask_account_card(operation.get('to', 'Неизвестно'))

    result = f"{date} {description}\n"

    # Если есть отправитель и получатель
    if from_account != 'Неизвестно' and to_account != 'Неизвестно':
        result += f"{from_account} -> {to_account}\n"
    elif from_account != 'Неизвестно':
        result += f"{from_account}\n"
    elif to_account != 'Неизвестно':
        result += f"{to_account}\n"

    result += f"Сумма: {amount} {currency}\n"

    return result


def main() -> None:
    """Основная логика программы работы с банковскими транзакциями."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # Выбор типа файла
    file_choice = input().strip()
    file_types = {"1": "JSON", "2": "CSV", "3": "XLSX"}

    if file_choice in file_types:
        print(f"Для обработки выбран {file_types[file_choice]}-файл.")
    else:
        print("Неверный выбор файла.")
        return

    # Загрузка данных из файла
    operations = load_operations(file_choice)

    if not operations:
        print("Не удалось загрузить операции. Программа завершена.")
        return

    # Фильтрация по статусу
    operations = filter_by_status(operations)

    if not operations:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Дополнительные фильтры
    operations = sort_operations(operations)
    operations = filter_rub_operations(operations)
    operations = filter_by_keyword(operations)

    if not operations:
        print("После применения фильтров не осталось операций")
        return

    # Вывод результатов
    print_operations(operations)


def filter_by_status(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрует операции по статусу."""
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

        status = input().strip().upper()

        if status in valid_statuses:
            filtered_operations = [
                op for op in operations
                if op.get('state', '').upper() == status
            ]
            print(f"Операции отфильтрованы по статусу '{status}'")
            return filtered_operations
        else:
            print(f"Статус операции '{status}' недоступен.")


def sort_operations(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Сортирует операции по дате."""
    answer = input("Отсортировать операции по дате? Да/Нет: ").strip().lower()

    if answer in ['да', 'yes', 'y', 'д']:
        order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()

        reverse = order == 'по убыванию'
        sorted_operations = sorted(
            operations,
            key=lambda x: x.get('date', ''),
            reverse=reverse
        )
        return sorted_operations

    return operations


def filter_rub_operations(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрует рублевые операции."""
    answer = input("Выводить только рублевые транзакции? Да/Нет: ").strip().lower()

    if answer in ['да', 'yes', 'y', 'д']:
        return [op for op in operations if op.get('currency', '').upper() == 'RUB']

    return operations


def filter_by_keyword(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрует операции по ключевому слову."""
    answer = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()

    if answer in ['да', 'yes', 'y', 'д']:
        keyword = input("Введите слово для поиска в описании: ").strip()
        return process_bank_search(operations, keyword)

    return operations


def print_operations(operations: List[Dict[str, Any]]) -> None:
    """Выводит отформатированный список операций."""
    print("\nРаспечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(operations)}\n")

    for i, operation in enumerate(operations, 1):
        print(f"--- Операция {i} ---")
        print(format_operation(operation))
        print()  # Пустая строка между операциями


if __name__ == "__main__":
    main()