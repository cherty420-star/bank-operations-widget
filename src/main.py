import csv
import json
import os
import random
from typing import Any, Dict, List

import pandas as pd

from src.operations import process_bank_operations, process_bank_search
from src.widget import mask_account_card, get_date


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
            operations = read_json_file(file_path)
        elif file_type == "2":  # CSV
            operations = read_csv_file(file_path)
        elif file_type == "3":  # XLSX
            operations = read_excel_file(file_path)

        if operations:
            print(f"✅ Успешно загружено {len(operations)} операций")

            # Отладочная информация о первых операциях
            print("🔍 Информация о первых 2 операциях:")
            for i, op in enumerate(operations[:2]):
                print(f"   Операция {i + 1}:")
                print(f"     - ID: {op.get('id')}")
                print(f"     - State: {op.get('state')}")
                print(f"     - Currency: '{op.get('currency')}'")
                print(f"     - Amount: {op.get('amount')}")
                print(f"     - Description: {op.get('description')}")

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

        processed_operations = []

        # Обрабатываем как список операций
        operations_list = data if isinstance(data, list) else data.get('operations', [])

        for operation in operations_list:
            # Создаем стандартизированную операцию
            processed_op = {
                'id': operation.get('id', 0),
                'state': operation.get('state', ''),
                'date': operation.get('date', ''),
                'description': operation.get('description', ''),
                'from': operation.get('from', ''),
                'to': operation.get('to', '')
            }

            # Обрабатываем amount и currency (вложенная структура)
            operation_amount = operation.get('operationAmount', {})
            if operation_amount and isinstance(operation_amount, dict):
                # Amount
                amount_str = operation_amount.get('amount', '0')
                try:
                    processed_op['amount'] = float(amount_str) if amount_str else 0.0
                except (ValueError, TypeError):
                    processed_op['amount'] = 0.0

                # Currency
                currency_info = operation_amount.get('currency', {})
                if currency_info and isinstance(currency_info, dict):
                    processed_op['currency'] = currency_info.get('code', 'RUB')
                else:
                    processed_op['currency'] = str(currency_info) if currency_info else 'RUB'
            else:
                # Если нет operationAmount, ищем на верхнем уровне
                processed_op['amount'] = operation.get('amount', 0.0)
                processed_op['currency'] = operation.get('currency', 'RUB')

            processed_operations.append(processed_op)

        return processed_operations

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
        # Заменяем NaN значения на пустые строки
        df = df.fillna('')
        operations = df.to_dict('records')

        # Обрабатываем типы данных
        for operation in operations:
            # Преобразуем числовые поля в строки
            if 'from' in operation:
                operation['from'] = str(operation['from']) if operation['from'] else ''
            if 'to' in operation:
                operation['to'] = str(operation['to']) if operation['to'] else ''
            if 'description' in operation:
                operation['description'] = str(operation['description']) if operation['description'] else ''

        return operations
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
    """
    answer = input("\nВыводить только рублевые транзакции? Да/Нет: ").strip().lower()

    if answer in ['да', 'yes', 'y', 'д']:
        rub_operations = [
            op for op in operations
            if str(op.get('currency', '')).upper() in ['RUB', 'RUR', 'РУБ', 'RU']
        ]
        print(f"Оставлено рублевых операций: {len(rub_operations)}")

        # Отладочная информация
        if rub_operations:
            print("💰 Примеры валют в отфильтрованных операциях:")
            for i, op in enumerate(rub_operations[:3]):  # покажем первые 3
                print(f"   Операция {i + 1}: валюта = '{op.get('currency')}', сумма = {op.get('amount')}")

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


def format_operation(operation: Dict[str, Any]) -> str:
    """
    Форматирует операцию для вывода используя импортированные функции.

    Args:
        operation: Данные операции

    Returns:
        str: Отформатированная строка операции
    """
    # Используем импортированную функцию get_date из widget.py
    date = get_date(operation.get('date', ''))
    description = operation.get('description', '')
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

    try:
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

    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")

if __name__ == "__main__":
    main()