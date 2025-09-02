"""Основной модуль для демонстрации функциональности банковских масок.

Этот модуль обеспечивает демонстрацию
функций маскировки номера карты и счета из модуля "Маски".
"""

from src.masks import get_mask_card_number, get_mask_account


def main() -> None:
    """Demonstrate the masking functions."""
    print("Демонстрация работы функций маскировки:")
    print()

    # Тест маскировки карт
    test_cards = [
        "1234567890123456",
        "1111222233334444",
        "5555666677778888"
    ]

    print("Маскировка номеров карт:")
    for card in test_cards:
        masked_card = get_mask_card_number(card)
        print(f"  {card} -> {masked_card}")

    print()

    # Тест маскировки счетов
    test_accounts = [
        "1234567890",
        "1111222233334444",
        "9988776655"
    ]

    print("Маскировка номеров счетов:")
    for account in test_accounts:
        masked_account = get_mask_account(account)
        print(f"  {account} -> {masked_account}")

    print()

    # Демонстрация обработки ошибок
    print("Проверка обработки ошибок:")
    try:
        get_mask_card_number("123")  # Слишком короткий номер
    except ValueError as e:
        print(f"  Ошибка карты: {e}")

    try:
        get_mask_account("12a")  # Не цифры
    except ValueError as e:
        print(f"  Ошибка счета: {e}")


if __name__ == "__main__":
    main()