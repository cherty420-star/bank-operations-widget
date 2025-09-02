def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в переданной строке.

    Args:
        account_info: строка с информацией о карте или счете
        (например: "Visa Platinum 7000792289606361", "Счет 73654108430135874305")

    Returns:
        str: строка с замаскированным номером
    """
    # Разделяем строку на части
    parts = account_info.split()

    # Если это счет
    if "счет" in account_info.lower():
        # Берем последнюю часть (номер счета)
        account_number = parts[-1]
        # Маскируем счет: показываем последние 4 цифры
        masked_number = f"**{account_number[-4:]}"
        return f"{' '.join(parts[:-1])} {masked_number}"

    else:
        # Это карта - берем последнюю часть (номер карты)
        card_number = parts[-1]
        # Маскируем карту: первые 6 и последние 4 цифры видимы
        if len(card_number) >= 16:
            masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        else:
            masked_number = card_number  # если номер слишком короткий

        return f"{' '.join(parts[:-1])} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ

    Args:
        date_string: строка с датой в формате "2024-03-11T02:26:18.671407"

    Returns:
        str: дата в формате "11.03.2024"
    """
    from datetime import datetime

    try:
        # Парсим дату из строки
        date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        # Форматируем в нужный формат
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        # Если формат неправильный, возвращаем оригинальную строку или обрабатываем ошибку
        return date_string