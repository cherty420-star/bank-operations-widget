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
        # Автоматически ищем файл в стандартных папках
        possible_paths = [
            file_path,  # исходный путь
            os.path.join('data', file_path),  # папка data
            os.path.join('..', 'data', file_path),  # на уровень выше в data
            os.path.join(os.path.dirname(__file__), '..', 'data', file_path)  # абсолютный путь
        ]

        actual_path = None
        for path in possible_paths:
            if os.path.exists(path):
                actual_path = path
                break

        if actual_path is None:
            print(f"Файл {file_path} не найден в стандартных расположениях:")
            for path in possible_paths:
                print(f"  - {path}")
            return []

        print(f"Загружаем данные из: {actual_path}")

        with open(actual_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Обработка разных форматов данных
        if isinstance(data, list):
            operations = data
        elif isinstance(data, dict):
            # Пробуем разные возможные ключи
            possible_keys = ['operations', 'transactions', 'data', 'results']
            operations = []
            for key in possible_keys:
                if key in data and isinstance(data[key], list):
                    operations = data[key]
                    break
            if not operations:
                operations = [data]  # если единственный словарь
        else:
            print("Неверный формат данных в JSON-файле")
            return []

        print(f"Успешно загружено {len(operations)} операций")
        return operations

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
    # Стандартные файлы из предыдущих домашних заданий
    default_files = {
        "1": "operations.json",  # JSON файл
        "2": "transactions.csv",  # CSV файл
        "3": "operations.xlsx"  # Excel файл
    }

    if file_type == "1":  # JSON
        file_name = input("Введите имя JSON-файла (по умолчанию: operations.json): ").strip()
        if not file_name:
            file_name = default_files["1"]

        operations = load_operations_from_json(file_name)

        if not operations:
            # Пробуем альтернативные имена файлов
            alternative_files = [
                "operations.json",
                "data.json",
                "transactions.json",
                "bank_operations.json"
            ]
            for alt_file in alternative_files:
                print(f"Пробуем загрузить {alt_file}...")
                operations = load_operations_from_json(alt_file)
                if operations:
                    break

        return operations

    elif file_type == "2":  # CSV
        print("Загрузка из CSV файлов будет реализована в будущем")
        file_name = input("Введите имя CSV-файла: ").strip()
        if not file_name:
            file_name = default_files["2"]
        print(f"CSV файл {file_name} будет обработан в будущих версиях")
        return []

    elif file_type == "3":  # XLSX
        print("Загрузка из XLSX файлов будет реализована в будущем")
        file_name = input("Введите имя XLSX-файла: ").strip()
        if not file_name:
            file_name = default_files["3"]
        print(f"Excel файл {file_name} будет обработан в будущих версиях")
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

    # Форматирование счета/карты
    from_account = operation.get('from', '')
    to_account = operation.get('to', '')

    result = f"{date} {description}\n"

    # Добавляем информацию об отправителе/получателе с маскировкой
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

    print(f"Загружено {len(operations)} операций для обработки.")

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
    """Сортирует операции по дате."""
    answer = input("\nОтсортировать операции по дате? Да/Нет: ").strip().lower()

    if answer in ['да', 'yes', 'y', 'д']:
        order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()

        reverse = order == 'по убыванию'

        # Фильтруем операции с датой
        operations_with_date = [op for op in operations if op.get('date')]
        operations_without_date = [op for op in operations if not op.get('date')]

        sorted_operations = sorted(
            operations_with_date,
            key=lambda x: x.get('date', ''),
            reverse=reverse
        )

        # Добавляем операции без даты в конец
        sorted_operations.extend(operations_without_date)

        order_text = "убыванию" if reverse else "возрастанию"
        print(f"Операции отсортированы по {order_text} даты")
        return sorted_operations

    return operations


def filter_rub_operations(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрует рублевые операции."""
    answer = input("\nВыводить только рублевые транзакции? Да/Нет: ").strip().lower()

    if answer in ['да', 'yes', 'y', 'д']:
        rub_operations = [op for op in operations if op.get('currency', '').upper() == 'RUB']
        print(f"Оставлено рублевых операций: {len(rub_operations)}")
        return rub_operations

    return operations


def filter_by_keyword(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрует операции по ключевому слову."""
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


def print_operations(operations: List[Dict[str, Any]]) -> None:
    """Выводит отформатированный список операций."""
    print("\n" + "=" * 50)
    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(operations)}\n")

    for i, operation in enumerate(operations, 1):
        print(f"--- Операция {i} ---")
        print(format_operation(operation))
        print()  # Пустая строка между операциями


if __name__ == "__main__":
    main()