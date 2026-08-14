import pytest

from src.search import process_bank_search, process_bank_operations


@pytest.fixture
def sample_data():
    """Фикстура с тестовыми данными банковских операций."""
    return [
        {"id": 1, "description": "Перевод организации", "amount": 100},
        {"id": 2, "description": "Оплата мобильной связи", "amount": 200},
        {"id": 3, "description": "Перевод организации", "amount": 300},
        {"id": 4, "amount": 400},  # Операция без описания
    ]


# --- Тесты для функции process_bank_search ---

def test_process_bank_search_success(sample_data):
    """Тест успешного поиска по регулярному выражению."""
    result = process_bank_search(sample_data, "перевод")
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_process_bank_search_empty_query(sample_data):
    """Тест возврата всех данных, если строка поиска пустая."""
    result = process_bank_search(sample_data, "")
    assert result == sample_data


def test_process_bank_search_no_match(sample_data):
    """Тест ситуации, когда совпадений не найдено."""
    result = process_bank_search(sample_data, "Вклад")
    assert result == []


def test_process_bank_search_special_characters(sample_data):
    """Тест корректной работы с экранированием спецсимволов."""
    result = process_bank_search(sample_data, ".*?")
    assert result == []


# --- Тесты для функции process_bank_operations ---

def test_process_bank_operations_count(sample_data):
    """Тест правильного подсчета количества операций по категориям."""
    categories = ["Перевод организации", "Оплата мобильной связи", "Открытие вклада"]
    result = process_bank_operations(sample_data, categories)

    assert result == {
        "Перевод организации": 2,
        "Оплата мобильной связи": 1,
        "Открытие вклада": 0
    }


def test_process_bank_operations_empty_categories(sample_data):
    """Тест с пустым списком категорий."""
    result = process_bank_operations(sample_data, [])
    assert result == {}
