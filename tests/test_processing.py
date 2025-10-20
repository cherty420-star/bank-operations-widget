# tests/test_processing.py
import pytest

from src.processing import filter_by_state, sort_by_date


class TestProcessing:
    @pytest.mark.parametrize("state, expected_count", [
        ('EXECUTED', 2),
        ('PENDING', 1),
        ('CANCELED', 1),
        ('UNKNOWN', 0)
    ])
    def test_filter_by_state(self, sample_operations, state, expected_count):
        result = filter_by_state(sample_operations, state)
        assert len(result) == expected_count
        if expected_count > 0:
            assert all(op['state'] == state for op in result)

    @pytest.mark.parametrize("reverse, first_id", [
        (True, 3),   # по убыванию - сначала последняя операция
        (False, 4)   # по возрастанию - сначала первая операция
    ])
    def test_sort_by_date(self, sample_operations, reverse, first_id):
        result = sort_by_date(sample_operations, reverse)
        assert result[0]['id'] == first_id
        assert result[-1]['id'] != first_id