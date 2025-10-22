from src.decorators import log


# Пример 1: Логирование в консоль
@log()
def calculate_sum(numbers: list) -> float:
    """Вычисляет сумму списка чисел"""
    return sum(numbers)


# Пример 2: Логирование в файл
@log(filename="operations.log")
def process_data(data: str) -> str:
    """Обрабатывает строку данных"""
    if not data:
        raise ValueError("Data cannot be empty")
    return data.upper()


# Демонстрация работы
if __name__ == "__main__":
    print("=== Демонстрация декоратора log ===")

    # Успешное выполнение в консоль
    print("\n1. Логирование в консоль (успех):")
    result1 = calculate_sum([1, 2, 3, 4, 5])
    print(f"Результат: {result1}")

    # Ошибка в консоль
    print("\n2. Логирование в консоль (ошибка):")
    try:
        process_data("")
    except ValueError as e:
        print(f"Поймано исключение: {e}")

    # Успешное выполнение в файл
    print("\n3. Логирование в файл (успех):")
    result2 = process_data("hello world")
    print(f"Результат: {result2}")

    print("\nПроверьте файл 'operations.log' для просмотра логов!")