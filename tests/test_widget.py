# tests/test_widget.py
import pytest
from src.widget import mask_account_card, get_date


class TestWidget:
    @pytest.mark.parametrize(
        "input_data, expected",
        [
            ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
            ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
            ("Счет 73654108430135874305", "Счет **4305"),
            ("Счет 12345678901234567890", "Счет **7890"),
            ("Visa Classic 1234567890123456", "Visa Classic 1234 56** **** 3456"),
            ("", ""),  # пустая строка
            ("Счет", "Счет"),  # только тип без номера
            ("Карта", "Карта"),  # только тип без номера
        ],
    )
    def test_mask_account_card(self, input_data, expected):
        """Тестирование маскировки карт и счетов с параметризацией"""
        assert mask_account_card(input_data) == expected

    @pytest.mark.parametrize(
        "input_date, expected",
        [
            ("2024-03-11T02:26:18.671407", "11.03.2024"),
            ("2023-12-31T23:59:59.999999", "31.12.2023"),
            ("2023-01-01T00:00:00.000000", "01.01.2023"),
            ("2022-02-28T15:30:45.123456", "28.02.2022"),
            ("2021-07-15T08:45:30.456789", "15.07.2021"),
            ("2020-11-05T12:00:00.000000", "05.11.2020"),
        ],
    )
    def test_get_date_valid(self, input_date, expected):
        """Тестирование форматирования даты с параметризацией"""
        assert get_date(input_date) == expected

    @pytest.mark.parametrize(
        "invalid_date",
        [
            "invalid-date-format",
            "2024/03/11T02:26:18.671407",  # неправильный разделитель
            "2024-03-11",  # без времени
            "02:26:18.671407",  # только время
            "",  # пустая строка
            None,  # None значение
        ],
    )
    def test_get_date_invalid(self, invalid_date):
        """Тестирование обработки невалидных дат"""
        # Функция должна возвращать исходную строку при ошибке
        assert get_date(invalid_date) == invalid_date

    def test_mask_account_card_edge_cases(self):
        """Тестирование крайних случаев для маскировки"""
        # Короткие номера карт
        assert mask_account_card("Visa 1234567890") == "Visa 1234 56** **** 7890"

        # Номера с пробелами
        assert mask_account_card("Visa Platinum  7000792289606361  ") == "Visa Platinum 7000 79** **** 6361"

    def test_get_date_edge_cases(self):
        """Тестирование крайних случаев для дат"""
        # Дата с Z в конце (UTC)
        assert get_date("2024-03-11T02:26:18.671407Z") == "11.03.2024"

        # Дата с часовым поясом
        assert get_date("2024-03-11T02:26:18.671407+03:00") == "11.03.2024"