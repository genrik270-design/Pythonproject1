import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_operations():
    """Тестовые данные для фильтрации и сортировки."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-12-18T10:15:30"},
        {"id": 2, "state": "CANCELED", "date": "2020-01-05T12:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2018-06-03T08:00:15"},
    ]


def test_filter_by_state(sample_operations):
    """Тест фильтрации по статусу."""
    result = filter_by_state(sample_operations, "EXECUTED")
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_filter_by_state_empty():
    """Тест фильтрации пустого списка."""
    assert filter_by_state([], "EXECUTED") == []


def test_sort_by_date_descending(sample_operations):
    """Тест сортировки по дате от самых новых к старым (по умолчанию)."""
    result = sort_by_date(sample_operations)
    assert result[0]["id"] == 2  # 2020 год
    assert result[1]["id"] == 1  # 2019 год
    assert result[2]["id"] == 3  # 2018 год


def test_sort_by_date_ascending(sample_operations):
    """Тест сортировки по дате по возрастанию (reverse=False)."""
    result = sort_by_date(sample_operations, reverse=False)
    assert result[0]["id"] == 3  # 2018 год
    assert result[1]["id"] == 1  # 2019 год
    assert result[2]["id"] == 2  # 2020 год
