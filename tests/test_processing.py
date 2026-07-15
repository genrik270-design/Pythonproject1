import pytest
from src.processing import filter_by_state, sort_by_date


# =====================================================================
# ФИКСТУРЫ ДЛЯ ТЕСТОВЫХ ДАННЫХ
# =====================================================================

@pytest.fixture
def standard_data():
    """Стандартный набор данных с разными статусами и последовательными датами."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2026-06-29T10:14:00"},
        {"id": 2, "state": "CANCELED", "date": "2026-06-28T12:00:00"},
        {"id": 3, "state": "PENDING", "date": "2026-06-30T09:00:00"},
    ]


@pytest.fixture
def edge_case_data():
    """Сложный набор данных: одинаковые даты, некорректный формат и пустая дата."""
    return [
        {"id": 10, "state": "EXECUTED", "date": "2026-07-14T12:00:00"},
        {"id": 11, "state": "EXECUTED", "date": "2026-07-14T12:00:00"},  # Одинаковая дата
        {"id": 12, "state": "CANCELED", "date": "bad-date-format"},  # Некорректный формат
        {"id": 13, "state": "EXECUTED", "date": ""},  # Пустая дата
    ]


# =====================================================================
# ТЕСТЫ ДЛЯ ФУНКЦИИ filter_by_state
# =====================================================================

# 1. Параметризация тестов для различных возможных значений статуса state
@pytest.mark.parametrize("target_state, expected_ids", [
    ("EXECUTED", [1]),
    ("CANCELED", [2]),
    ("PENDING", [3]),
])
def test_filter_by_state_valid(standard_data, target_state, expected_ids):
    """Тестирование фильтрации списка словарей по заданному статусу state."""
    result = filter_by_state(standard_data, state=target_state)
    result_ids = [item["id"] for item in result]
    assert result_ids == expected_ids


# 2. Проверка работы функции при отсутствии словарей с указанным статусом
def test_filter_by_state_no_match(standard_data):
    """Проверка работы функции при отсутствии словарей с указанным статусом state в списке."""
    result = filter_by_state(standard_data, state="NON_EXISTENT")
    assert result == []


# =====================================================================
# ТЕСТЫ ДЛЯ ФУНКЦИИ sort_by_date
# =====================================================================

# 1. Тестирование сортировки по убыванию и возрастанию
def test_sort_by_date_order(standard_data):
    """Тестирование сортировки списка словарей по датам в порядке убывания и возрастания."""
    # По убыванию (от свежих к старым — по умолчанию)
    descending = sort_by_date(standard_data)
    assert descending[0]["id"] == 3  # 30 июня
    assert descending[1]["id"] == 1  # 29 июня
    assert descending[2]["id"] == 2  # 28 июня

    # По возрастанию (от старых к свежим)
    ascending = sort_by_date(standard_data, reverse=False)
    assert ascending[0]["id"] == 2  # 28 июня
    assert ascending[1]["id"] == 1  # 29 июня
    assert ascending[2]["id"] == 3  # 30 июня


# 2. Проверка корректности сортировки при одинаковых датах
def test_sort_by_date_identical(edge_case_data):
    """Проверка корректности сортировки при одинаковых датах."""
    # Берем только два элемента с одинаковыми датами
    identical_items = [edge_case_data[0], edge_case_data[1]]
    result = sort_by_date(identical_items)

    # Сортировка должна пройти успешно и вернуть оба элемента
    assert len(result) == 2
    assert result[0]["id"] in [10, 11]


# 3. Тесты на работу функции с некорректными или нестандартными форматами дат
def test_sort_by_date_invalid_formats(edge_case_data):
    """Проверка, что элементы с битыми или пустыми датами безопасно уходят в конец при reverse=True."""
    result = sort_by_date(edge_case_data, reverse=True)

    # Корректные даты (14 июля) должны быть в самом начале списка
    assert result[0]["id"] in [10, 11]
    assert result[1]["id"] in [10, 11]

    # Словари с ошибками (id 12 и 13) получили datetime.min, поэтому они оказались в хвосте
    assert result[2]["id"] in [12, 13]
    assert result[3]["id"] in [12, 13]