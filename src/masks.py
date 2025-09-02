"""Module for masking banking card and account numbers."""


def get_mask_card_number(card_number: str) -> str:
    """
    Mask a banking card number by showing first 6 and last 4 digits.

    The function takes a 16-digit card number and returns it in masked format:
    XXXX XX** **** XXXX

    Args:
        card_number (str): A string containing exactly 16 digits representing the card number.

    Returns:
        str: Masked card number in the format "XXXX XX** **** XXXX".

    Raises:
        ValueError: If the card number is not exactly 16 digits long or contains non-digit characters.

    Example:
        >>> get_mask_card_number("1234567890123456")
        '1234 56** **** 3456'
    """
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("Card number must be 16 digits")

    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Mask a bank account number by showing only the last 4 digits.

    The function takes an account number and returns it in masked format:
    **XXXX

    Args:
        account_number (str): A string containing at least 4 digits representing the account number.

    Returns:
        str: Masked account number in the format "**XXXX".

    Raises:
        ValueError: If the account number has less than 4 digits or contains non-digit characters.

    Example:
        >>> get_mask_account("1234567890")
        '**7890'
    """
    if len(account_number) < 4 or not account_number.isdigit():
        raise ValueError("Account number must be at least 4 digits")

    return f"**{account_number[-4:]}"