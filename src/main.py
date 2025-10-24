from typing import List, Dict, Any
import os
import json
from widget import mask_account_card, get_date
from operations import process_bank_search

def load_operations_from_json() -> List[Dict[str, Any]]:
    """
    Загружает операции из JSON-файла.
    """
    possible_paths = [
        "operations.json",
        "data/operations.json",
        "../data/operations.json",
        os.path.join(os.path.dirname(__file__), '..', 'data', 'operations.json')
    ]

    for file_path in possible_paths:
        try:
            if os.path.exists(file_path):
                print(f"Загружаем данные из: {file_path}")
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                if isinstance(data, list):
                    operations = data
                elif isinstance(data, dict):
                    possible_keys = ['operations', 'transactions', 'data']
                    operations = []
                    for key in possible_keys:
                        if key in data and isinstance(data[key], list):
                            operations = data[key]
                            break
                    if not operations:
                        operations = [data]
                else:
                    continue

                print(f"Успешно загружено {len(operations)} операций")
                return operations

        except Exception as e:
            continue

    print("Не удалось найти или загрузить файл operations.json")
    return []


def load_operations(file_type: str) -> List[Dict[str, Any]]:
    """
    Загружает операции из файла.
    """
    file_types = {"1": "JSON", "2": "CSV", "3": "XLSX"}

    if file_type in file_types:
        print(f"Для обработки выбран {file_types[file_type]}-файл.")
        return load_operations_from_json()

    return []


def filter_by_status(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Фильтрует операции по статусу.
    """
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

        status = input().strip().upper()

        if status in valid_statuses:
            filtered_operations = [
                op for op in operations
                if op.get('state', '').upper() == status
            ]
            print(f"Операции отфильтрованы по статусу '{status}'")
            print(f"Найдено операций: {len(filtered_operations)}")
            return filtered_operations
        else:
            print(f"Статус операции '{status}' недоступен.")


def sort_operations(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Сортирует операции по дате.
    """
    answer = input("\nОтсортировать операции по дате? Да/Нет: ").strip().lower()

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
    """
    Фильтрует рублевые операции.
    """
    answer = input("\nВыводить только рублевые транзакции? Да/Нет: ").strip().lower()

    if answer in ['да', 'yes', 'y', 'д']:
        return [op for op in operations if op.get('currency', '').upper() == 'RUB']

    return operations


def filter_by_keyword(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Фильтрует операции по ключевому слову.
    """
    answer = input("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()

    if answer in ['да', 'yes', 'y', 'д']:
        keyword = input("Введите слово для поиска в описании: ").strip()
        return process_bank_search(operations, keyword)

    return operations


def format_operation(operation: Dict[str, Any]) -> str:
    """
    Форматирует операцию для вывода.
    """
    date = get_date(operation.get('date', ''))
    description = operation.get('description', '')
    amount = operation.get('amount', 0)
    currency = operation.get('currency', 'RUB')

    from_account = operation.get('from', '')
    to_account = operation.get('to', '')

    result = f"{date} {description}\n"

    if from_account:
        result += f"{mask_account_card(from_account)}"
        if to_account:
            result += " -> "

    if to_account:
        result += f"{mask_account_card(to_account)}"

    if from_account or to_account:
        result += "\n"

    result += f"Сумма: {amount} {currency}\n"

    return result


def print_operations(operations: List[Dict[str, Any]]) -> None:
    """
    Выводит отформатированный список операций.
    """
    print("\n" + "=" * 50)
    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(operations)}\n")

    for i, operation in enumerate(operations, 1):
        print(f"--- Операция {i} ---")
        print(format_operation(operation))
        print()


def main() -> None:
    """
    Основная логика программы работы с банковскими транзакциями.
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_choice = input().strip()
    operations = load_operations(file_choice)

    if not operations:
        print("Не удалось загрузить операции. Программа завершена.")
        return

    operations = filter_by_status(operations)

    if not operations:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    operations = sort_operations(operations)
    operations = filter_rub_operations(operations)
    operations = filter_by_keyword(operations)

    if not operations:
        print("После применения фильтров не осталось операций")
        return

    print_operations(operations)


if __name__ == "__main__":
    main()