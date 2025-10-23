from typing import List, Dict, Any
import os
import json
from widget import mask_account_card, get_date
from operations import process_bank_search


def load_operations_from_json() -> List[Dict[str, Any]]:
    """
    Загружает операции из JSON-файла по умолчанию.

    Returns:
        List[Dict]: Список операций
    """
    # Стандартные пути к файлам
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
                    continue

                print(f"Успешно загружено {len(operations)} операций")
                return operations

        except Exception as e:
            continue

    print("Не удалось найти или загрузить файл operations.json")
    return []


def load_operations(file_type: str) -> List[Dict[str, Any]]:
    """
    Загружает операции из JSON файла независимо от выбора.
    CSV и Excel будут добавлены в будущем.
    """
    file_types = {"1": "JSON", "2": "CSV", "3": "XLSX"}
    selected_type = file_types.get(file_type, "JSON")

    print(f"Для обработки выбран {selected_type}-файл.")

    # Всегда загружаем из JSON для демонстрации
    operations = load_operations_from_json()

    if not operations:
        print("Не удалось загрузить данные.")

    return operations


def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """
    Конвертирует валюту (упрощенная реализация).

    Args:
        amount: Сумма
        from_currency: Исходная валюта
        to_currency: Целевая валюта

    Returns:
        float: Конвертированная сумма
    """
    if from_currency == to_currency:
        return amount

    # Упрощенные курсы для демонстрации
    exchange_rates = {
        'USD': {'RUB': 90.0, 'EUR': 0.85},
        'EUR': {'USD': 1.18, 'RUB': 95.0},
        'RUB': {'USD': 0.011, 'EUR': 0.0105}
    }

    if from_currency in exchange_rates and to_currency in exchange_rates[from_currency]:
        return amount * exchange_rates[from_currency][to_currency]
    else:
        # Если курс неизвестен, возвращаем исходную сумму
        return amount


def format_operation(operation: Dict[str, Any], target_currency: str = None) -> str:
    """
    Форматирует операцию для красивого вывода.

    Args:
        operation: Данные операции
        target_currency: Валюта для конвертации (None - исходная валюта)

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

    # Конвертация валюты если нужно
    if target_currency and target_currency != currency:
        converted_amount = convert_currency(amount, currency, target_currency)
        amount_display = f"{converted_amount:.2f}"
        currency_display = target_currency
        original_info = f" (оригинал: {amount} {currency})"
    else:
        amount_display = amount
        currency_display = currency
        original_info = ""

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

    result += f"Сумма: {amount_display} {currency_display}{original_info}\n"

    return result


def debug_operations(operations: List[Dict[str, Any]]):
    """Показывает отладочную информацию о операциях."""
    if not operations:
        print("Нет операций для отладки")
        return

    print("\n=== ОТЛАДОЧНАЯ ИНФОРМАЦИЯ ===")
    print(f"Всего операций: {len(operations)}")

    # Покажем первые 3 операции для анализа структуры
    for i, op in enumerate(operations[:3], 1):
        print(f"\nОперация {i}:")
        for key, value in op.items():
            print(f"  {key}: {value}")

    # Статистика по статусам
    status_counts = {}
    for op in operations:
        state = op.get('state') or op.get('status') or op.get('State') or op.get('Status') or 'UNKNOWN'
        status_counts[state] = status_counts.get(state, 0) + 1

    print(f"\nСтатистика по статусам: {status_counts}")
    print("============================\n")


def filter_by_status(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрует операции по статусу."""
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

        status = input().strip().upper()

        if status in valid_statuses:
            # Пробуем разные возможные названия полей для статуса
            filtered_operations = []
            for op in operations:
                # Пробуем разные варианты названий поля статуса
                state = op.get('state') or op.get('status') or op.get('State') or op.get('Status')
                if state and state.upper() == status:
                    filtered_operations.append(op)

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


def filter_currency_operations(operations: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], str]:
    """Фильтрует операции по валюте с возможностью конвертации."""
    answer = input("\nФильтровать по валюте? Да/Нет: ").strip().lower()

    if answer in ['да', 'yes', 'y', 'д']:
        print("Доступные валюты: RUB, USD, EUR, ALL (все валюты)")
        currency_choice = input("Введите валюту (или ALL для всех): ").strip().upper()

        if currency_choice == 'ALL':
            target_currency = input("В какую валюту конвертировать? (RUB/USD/EUR): ").strip().upper()
            if target_currency not in ['RUB', 'USD', 'EUR']:
                target_currency = None
            print(f"Показаны все валюты, конвертация в {target_currency if target_currency else 'исходные валюты'}")
            return operations, target_currency
        else:
            filtered_operations = [op for op in operations if op.get('currency', '').upper() == currency_choice]
            print(f"Оставлено операций в валюте {currency_choice}: {len(filtered_operations)}")
            return filtered_operations, currency_choice

    return operations, None


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


def print_operations(operations: List[Dict[str, Any]], target_currency: str = None) -> None:
    """Выводит отформатированный список операций."""
    print("\n" + "=" * 50)
    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(operations)}\n")

    for i, operation in enumerate(operations, 1):
        print(f"--- Операция {i} ---")
        print(format_operation(operation, target_currency))
        print()  # Пустая строка между операциями


def main() -> None:
    """Основная логика программы работы с банковскими транзакциями."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # Выбор типа файла
    file_choice = input().strip()

    if file_choice not in ["1", "2", "3"]:
        print("Неверный выбор файла.")
        return

    # Загрузка данных из файла
    operations = load_operations(file_choice)

    if not operations:
        print("Не удалось загрузить операции. Программа завершена.")
        return

    print(f"Загружено {len(operations)} операций для обработки.")

    # ПОКАЗАТЬ ОТЛАДОЧНУЮ ИНФОРМАЦИЮ
    debug_operations(operations)

    # Фильтрация по статусу
    operations = filter_by_status(operations)

    if not operations:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Дополнительные фильтры
    operations = sort_operations(operations)
    operations, target_currency = filter_currency_operations(operations)
    operations = filter_by_keyword(operations)

    if not operations:
        print("После применения фильтров не осталось операций")
        return

    # Вывод результатов
    print_operations(operations, target_currency)


if __name__ == "__main__":
    main()