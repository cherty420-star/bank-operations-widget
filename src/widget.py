def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер счета или карты.
    Для карт: первые 6 и последние 4 цифры видимы, остальные заменены на *
    Для счетов: видимы только последние 4 цифры
    """
    if not account_info or not any(char.isdigit() for char in account_info):
        return account_info

    # Разделяем текст и цифры
    words = account_info.split()
    digits = ''.join([char for char in account_info if char.isdigit()])
    text = ' '.join([word for word in words if not word.isdigit()])

    if not digits:
        return account_info

    # Определяем тип по тексту или длине цифр
    if ("счет" in text.lower() or "account" in text.lower() or
            len(digits) > 16):  # Считаем, что счета длиннее 16 цифр

        # Маскировка счета: показываем только последние 4 цифры
        if len(digits) >= 4:
            masked_digits = "**" + digits[-4:]
        else:
            masked_digits = digits
    else:
        # Маскировка карты: показываем первые 6 и последние 4 цифры
        if len(digits) >= 10:
            # Для нормальных номеров карт
            first_six = digits[:6]
            last_four = digits[-4:]
            middle = "*" * max(0, len(digits) - 10)  # Звездочки для средней части
            masked_digits = f"{first_six[:4]} {first_six[4:6]}{middle} {last_four}"
        elif len(digits) >= 8:
            # Для коротких номеров - адаптивная маскировка
            first_part = digits[:4]
            last_part = digits[-4:]
            middle = "*" * max(0, len(digits) - 8)
            masked_digits = f"{first_part} {middle} {last_part}"
        else:
            # Для очень коротких номеров - не маскируем
            masked_digits = digits

    return f"{text} {masked_digits}".strip() if text else masked_digits

def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ

    Args:
        date_string: строка с датой в формате "2024-03-11T02:26:18.671407"

    Returns:
        str: дата в формате "11.03.2024" или исходная строка при ошибке
    """
    from datetime import datetime

    # Проверка на None и пустую строку
    if date_string is None:
        return None
    if date_string == "":
        return ""

    try:
        # Проверяем, содержит ли строка время (буква 'T' или время с миллисекундами)
        if 'T' not in date_string and '.' not in date_string and len(date_string) == 10:
            # Это просто дата без времени - возвращаем как есть
            return date_string

        # Парсим дату из строки ISO формата
        date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        # Форматируем в нужный формат
        return date_obj.strftime("%d.%m.%Y")
    except (ValueError, AttributeError):
        # При любой ошибке возвращаем исходную строку
        return date_string