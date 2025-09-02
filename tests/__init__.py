"""Модуль для маскировки номеров карт и счетов."""

def get_mask_card_number(card_number: str) -> str:
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("Card number must be 16 digits")

    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

def get_mask_account(account_number: str) -> str:
    if len(account_number) < 4 or not account_number.isdigit():
        raise ValueError("Account number must be at least 4 digits")

    return f"**{account_number[-4:]}"