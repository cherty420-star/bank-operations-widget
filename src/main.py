import os
import random
from typing import Any, Dict, List

from src.utils.file_reader import read_transactions_from_json, read_csv_file, read_excel_file
from src.processing import filter_by_state, sort_by_date
from src.widget import mask_account_card, get_date
from src.operations import process_bank_search, process_bank_operations


def get_file_path(filename: str) -> str:
    """
    Возвращает абсолютный путь к файлу в папке data.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, "data", filename)


def load_operations(file_type: str) -> List[Dict[str, Any]]:
    """
    Загружает операции из файла используя существующие функции.
    """
    file_types = {"1": "JSON", "2": "CSV", "3": "XLSX"}

    if file_type not in file_types:
        print("❌ Неверный выбор файла. Доступны только варианты 1, 2, 3")
        return []

    print(f"Для обработки выбран {file_types[file_type]}-файл.")

    # Определяем пути к файлам
    file_paths = {
        "1": get_file_path("operations.json"),
        "2": get_file_path("transactions.csv"),
        "3": get_file_path("operations.xlsx")
    }

    file_path = file_paths.get(file_type)

    if not file_path:
        print("❌ Путь к файлу не определен")
        return []

    # Проверяем существование файла
    if not os.path.exists(file_path):
        print(f"❌ Файл не найден: {file_path}")
        return []

    try:
        operations = []
        if file_type == "1":  # JSON
            # ИСПОЛЬЗУЕМ существующую функцию read_transactions_from_json
            operations = read_transactions_from_json(file_path)
        elif file_type == "2":  # CSV
            # ИСПОЛЬЗУЕМ новую функцию read_csv_file
            operations = read_csv_file(file_path)
        elif file_type == "3":  # XLSX
            # ИСПОЛЬЗУЕМ новую функцию read_excel_file
            operations = read_excel_file(file_path)

        if operations:
            print(f"✅ Успешно загружено {len(operations)} операций")
            return operations
        else:
            print("⚠️ Файл загружен, но не содержит операций")
            return []

    except Exception as e:
        print(f"❌ Ошибка загрузки данных: {e}")
        return []


def filter_by_status(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Фильтрует операции по статусу используя существующую функцию.
    """
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

        status = input().strip().upper()

        if not status:
            print("Статус не может быть пустым")
            continue

        if status in valid_statuses:
            # ИСПОЛЬЗУЕМ существующую функцию filter_by_state
            filtered_operations = filter_by_state(operations, status)
            print(f"Операции отфильтрованы по статусу '{status}'")
            print(f"Найдено операций: {len(filtered_operations)}")
            return filtered_operations
        else:
            print(f"Статус операции '{status}' недоступен.")


def sort_operations(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Сортирует операции по дате используя существующую функцию.
    """
    answer = input("\nОтсортировать операции по дате? Да/Нет: ").strip().lower()

    if answer in ['да', 'yes', 'y', 'д']:
        while True:
            order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()

            if order in ['по возрастанию', 'возрастанию']:
                # ИСПОЛЬЗУЕМ существующую функцию sort_by_date
                sorted_operations = sort_by_date(operations, reverse=False)
                print("Операции отсортированы по возрастанию даты")
                return sorted_operations
            elif order in ['по убыванию', 'убыванию']:
                # ИСПОЛЬЗУЕМ существующую функцию sort_by_date
                sorted_operations = sort_by_date(operations, reverse=True)
                print("Операции отсортированы по убыванию даты")
                return sorted_operations
            else:
                print("Пожалуйста, введите 'по возрастанию' или 'по убыванию'")

    return operations


def filter_rub_operations(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Фильтрует рублевые операции.
    """
    answer = input("\nВыводить только рублевые транзакции? Да/Нет: ").strip().lower()

    if answer in ['да', 'yes', 'y', 'д']:
        rub_operations = [
            op for op in operations
            if str(op.get('currency', '')).upper() in ['RUB', 'RUR', 'РУБ', 'RU']
        ]
        print(f"Оставлено рублевых операций: {len(rub_operations)}")
        return rub_operations

    return operations


def filter_by_keyword(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Фильтрует операции по ключевому слову с использованием регулярных выражений.
    """
    answer = input("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()

    if answer in ['да', 'yes', 'y', 'д']:
        keyword = input("Введите слово для поиска в описании: ").strip()
        if keyword:
            filtered = process_bank_search(operations, keyword)
            print(f"Найдено операций с '{keyword}': {len(filtered)}")
            return filtered
        else:
            print("Пустой поисковый запрос")

    return operations


def format_operation(operation: Dict[str, Any]) -> str:
    """
    Форматирует операцию для вывода используя импортированные функции.
    """
    # Используем импортированную функцию get_date из widget.py
    date = get_date(operation.get('date', ''))
    description = operation.get('description', '')

    # ОБРАБАТЫВАЕМ СУММУ И ВАЛЮТУ (вложенная структура)
    amount = 0
    currency = 'RUB'

    # Проверяем вложенную структуру operationAmount
    operation_amount = operation.get('operationAmount')
    if operation_amount and isinstance(operation_amount, dict):
        amount = operation_amount.get('amount', 0)
        currency_info = operation_amount.get('currency', {})
        if isinstance(currency_info, dict):
            currency = currency_info.get('code', 'RUB')
        else:
            currency = str(currency_info) if currency_info else 'RUB'
    else:
        # Если нет operationAmount, ищем на верхнем уровне
        amount = operation.get('amount', 0)
        currency = operation.get('currency', 'RUB')

    from_account = operation.get('from', '')
    to_account = operation.get('to', '')

    result = f"{date} {description}\n"

    # Используем импортированную функцию mask_account_card из widget.py
    if from_account:
        # Преобразуем в строку на случай, если это число
        from_str = str(from_account) if not isinstance(from_account, str) else from_account
        result += f"{mask_account_card(from_str)}"
        if to_account:
            result += " -> "

    if to_account:
        # Преобразуем в строку на случай, если это число
        to_str = str(to_account) if not isinstance(to_account, str) else to_account
        result += f"{mask_account_card(to_str)}"

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
    print("Привет! Добро пожаловать в программу работы с банковскими транзакции.")

    print("\nВыберите необходимый пункт меню:")
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