from typing import List, Dict, Any
from widget import mask_account_card, get_date
from operations import process_bank_search


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

    # Здесь должна быть загрузка данных из файла
    # operations = load_operations(file_choice)
    operations: List[Dict[str, Any]] = []  # Добавляем аннотацию типа

    # Фильтрация по статусу
    operations = filter_by_status(operations)

    if not operations:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Дополнительные фильтры
    operations = sort_operations(operations)
    operations = filter_rub_operations(operations)
    operations = filter_by_keyword(operations)

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
    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(operations)}\n")

    for operation in operations:
        # Форматирование даты
        date = get_date(operation.get('date', ''))

        # Форматирование описания
        description = operation.get('description', '')

        # Форматирование суммы и валюты
        amount = operation.get('amount', 0)
        currency = operation.get('currency', 'RUB')

        print(f"{date} {description}")
        # Здесь должна быть логика маскировки счетов/карт
        # print(f"Счет **4321")
        print(f"Сумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()