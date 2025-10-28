import csv
import json
import os
import random
from typing import Any, Dict, List

import pandas as pd

from src.operations import process_bank_operations, process_bank_search


def get_file_path(filename: str) -> str:
    """
    Возвращает абсолютный путь к файлу в папке data.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, "data", filename)


def load_operations(file_type: str) -> List[Dict[str, Any]]:
    """
    Загружает операции из файла.
    """
    file_types = {"1": "JSON", "2": "CSV", "3": "XLSX"}

    if file_type not in file_types:
        print("❌ Неверный выбор файла")
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

    try:
        operations = []
        if file_type == "1":  # JSON
            operations = read_json_file(file_path)
        elif file_type == "2":  # CSV
            operations = read_csv_file(file_path)
        elif file_type == "3":  # XLSX
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


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """Читает JSON файл с операциями."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except Exception as e:
        print(f"Ошибка чтения JSON файла: {e}")
        return []


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """Читает CSV файл с операциями."""
    try:
        operations = []
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                operation = {
                    'id': int(row['id']) if row.get('id') and row['id'].strip().isdigit() else 0,
                    'state': row.get('state', ''),
                    'date': row.get('date', ''),
                    'amount': float(row['amount']) if row.get('amount') and row['amount'].strip() else 0.0,
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
    """Читает Excel файл с операциями."""
    try:
        df = pd.read_excel(file_path)
        return df.to_dict('records')
    except Exception as e:
        print(f"Ошибка чтения Excel файла: {e}")
        return []


def filter_by_status(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Фильтрует операции по статусу.

    Args:
        operations: Список операций

    Returns:
        List[Dict]: Отфильтрованный список операций
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

    Args:
        operations: Список операций

    Returns:
        List[Dict]: Отсортированный список операций
    """
    answer = input("\nОтсортировать операции по дате? Да/Нет: ").strip().lower()

    if answer in ['да', 'yes', 'y', 'д']:
        while True:
            order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()

            if order in ['по возрастанию', 'возрастанию']:
                sorted_operations = sorted(
                    operations,
                    key=lambda x: x.get('date', ''),
                    reverse=False
                )
                print("Операции отсортированы по возрастанию даты")
                return sorted_operations
            elif order in ['по убыванию', 'убыванию']:
                sorted_operations = sorted(
                    operations,
                    key=lambda x: x.get('date', ''),
                    reverse=True
                )
                print("Операции отсортированы по убыванию даты")
                return sorted_operations
            else:
                print("Пожалуйста, введите 'по возрастанию' или 'по убыванию'")

    return operations


def filter_rub_operations(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Фильтрует рублевые операции.

    Args:
        operations: Список операций

    Returns:
        List[Dict]: Отфильтрованный список операций
    """
    answer = input("\nВыводить только рублевые транзакции? Да/Нет: ").strip().lower()

    if answer in ['да', 'yes', 'y', 'д']:
        rub_operations = [
            op for op in operations
            if str(op.get('currency', '')).upper() == 'RUB'
        ]
        print(f"Оставлено рублевых операций: {len(rub_operations)}")
        return rub_operations

    return operations


def filter_by_keyword(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Фильтрует операции по ключевому слову с использованием регулярных выражений.

    Args:
        operations: Список операций

    Returns:
        List[Dict]: Отфильтрованный список операций
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


def get_random_operation_sample(operations: List[Dict[str, Any]], sample_size: int = 3) -> List[Dict[str, Any]]:
    """
    Возвращает случайную выборку операций.

    Args:
        operations: Список операций
        sample_size: Размер выборки

    Returns:
        List[Dict]: Случайная выборка операций
    """
    if len(operations) <= sample_size:
        return operations

    return random.sample(operations, sample_size)


def show_category_statistics(operations: List[Dict[str, Any]]) -> None:
    """
    Показывает статистику по категориям операций.

    Args:
        operations: Список операций
    """
    answer = input("\nПоказать статистику по категориям операций? Да/Нет: ").strip().lower()

    if answer in ['да', 'yes', 'y', 'д']:
        categories_input = input("Введите категории для анализа (через запятую): ").strip()
        if categories_input:
            categories = [cat.strip() for cat in categories_input.split(',')]
            statistics = process_bank_operations(operations, categories)

            print("\nСтатистика по категориям:")
            print("-" * 30)
            for category, count in statistics.items():
                print(f"{category}: {count} операций")


def mask_account_card(account_info: Any) -> str:
    """
    Маскирует номер счета или карты.

    Args:
        account_info: Информация о счете/карте (может быть строкой, числом или None)

    Returns:
        str: Замаскированная информация
    """
    if not account_info:
        return ""

    # Преобразуем в строку, если это число
    account_str = str(account_info) if not isinstance(account_info, str) else account_info

    if "Счет" in account_str:
        # Маскировка счета: показываем последние 4 цифры
        numbers = ''.join(filter(str.isdigit, account_str))
        if len(numbers) >= 4:
            return f"Счет **{numbers[-4:]}"
        return account_str
    else:
        # Маскировка карты: показываем первые 6 и последние 4 цифры
        numbers = ''.join(filter(str.isdigit, account_str))
        if len(numbers) == 16:
            card_name = account_str.split()[0] if ' ' in account_str else "Карта"
            return f"{card_name} {numbers[:4]} {numbers[4:6]}** **** {numbers[-4:]}"
        return account_str


def get_date(date_string: str) -> str:
    """
    Форматирует дату из ISO формата в DD.MM.YYYY.

    Args:
        date_string: Дата в формате ISO

    Returns:
        str: Отформатированная дата
    """
    try:
        if 'T' in date_string:
            date_part = date_string.split('T')[0]
            year, month, day = date_part.split('-')
            return f"{day}.{month}.{year}"
        return date_string
    except Exception:
        return date_string


def format_operation(operation: Dict[str, Any]) -> str:
    """
    Форматирует операцию для вывода.

    Args:
        operation: Данные операции

    Returns:
        str: Отформатированная строка операции
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

    Args:
        operations: Список операций
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

    # Показываем статистику по категориям
    show_category_statistics(operations)

    # Предлагаем случайную выборку
    if len(operations) > 3:
        show_sample = input("\nПоказать случайную выборку из 3 операций? Да/Нет: ").strip().lower()
        if show_sample in ['да', 'yes', 'y', 'д']:
            operations = get_random_operation_sample(operations, 3)
            print("Показана случайная выборка из 3 операций")

    if not operations:
        print("После применения фильтров не осталось операций")
        return

    print_operations(operations)


if __name__ == "__main__":
    main()