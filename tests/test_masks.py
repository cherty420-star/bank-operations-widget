"""Тесты для модуля масок."""

import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number_valid() -> None:
    """Test valid card number masking."""
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"
    assert get_mask_card_number("1111222233334444") == "1111 22** **** 4444"


def test_get_mask_account_valid() -> None:
    """Test valid account number masking."""
    assert get_mask_account("1234567890") == "**7890"
    assert get_mask_account("1111222233334444") == "**4444"


def test_get_mask_card_number_invalid() -> None:
    """Test invalid card number handling."""
    with pytest.raises(ValueError, match="Card number must be 16 digits"):
        get_mask_card_number("123")  # Too short

    with pytest.raises(ValueError, match="Card number must be 16 digits"):
        get_mask_card_number("12345678901234567")  # Too long

    with pytest.raises(ValueError, match="Card number must be 16 digits"):
        get_mask_card_number("123456789012abc6")  # Contains letters


def test_get_mask_account_invalid() -> None:
    """Test invalid account number handling."""
    with pytest.raises(ValueError, match="Account number must be at least 4 digits"):
        get_mask_account("123")  # Too short

    with pytest.raises(ValueError, match="Account number must be at least 4 digits"):
        get_mask_account("12ab")  # Contains letters