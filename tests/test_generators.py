import pytest
from src.generators import filter_transactions_by_currency, transaction_descriptions, card_number_generator

# Фикстура с тестовыми данными для переиспользования
@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 1,
            "description": "Перевод организации",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}}
        },
        {
            "id": 2,
            "description": "Перевод частному лицу",
            "operationAmount": {"amount": "150.00", "currency": {"name": "USD", "code": "USD"}}
        },
        {
            "id": 3,
            "description": "Покупка авиабилетов",
            "operationAmount": {"amount": "10500.00", "currency": {"name": "руб.", "code": "RUB"}}
        },
        {
            "id": 4  # Транзакция без описания и суммы для проверки на ошибки
        }
    ]


# --- Тесты для filter_transactions_by_currency ---

def test_filter_transactions_by_currency_rub(sample_transactions):
    """Проверка фильтрации транзакций по валюте RUB."""
    result = list(filter_transactions_by_currency(sample_transactions, "RUB"))
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_filter_transactions_by_currency_usd(sample_transactions):
    """Проверка фильтрации транзакций по валюте USD."""
    result = list(filter_transactions_by_currency(sample_transactions, "USD"))
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_filter_transactions_by_currency_empty():
    """Проверка работы с пустым списком."""
    result = list(filter_transactions_by_currency([], "RUB"))
    assert result == []


# --- Тесты для transaction_descriptions ---

def test_transaction_descriptions(sample_transactions):
    """Проверка извлечения описаний транзакций, включая случай отсутствия ключа."""
    generator = transaction_descriptions(sample_transactions)

    assert next(generator) == "Перевод организации"
    assert next(generator) == "Перевод частному лицу"
    assert next(generator) == "Покупка авиабилетов"
    assert next(generator) == "Описание отсутствует"


# --- Тесты для card_number_generator ---

def test_card_number_generator_format():
    """Проверка корректности формата генерируемых номеров карт."""
    generator = card_number_generator(1, 2)

    assert next(generator) == "0000 0000 0000 0001"
    assert next(generator) == "0000 0000 0000 0002"


def test_card_number_generator_range():
    """Проверка генерации правильного количества карт в диапазоне."""
    result = list(card_number_generator(10, 15))
    assert len(result) == 6  # Включая границы 10 и 15
    assert result[-1] == "0000 0000 0000 0015"


def test_filter_transactions_by_currency_invalid_data():
        """Проверка обработки некорректных данных (вызов AttributeError)."""
        invalid_data = [
            {"operationAmount": "не словарь, а строка"},  # Вызовет AttributeError при .get()
            None,  # Тоже вызовет ошибку
            {"operationAmount": {"currency": None}}  # И это сломает вложенный .get()
        ]
        result = list(filter_transactions_by_currency(invalid_data, "USD"))
        assert result == []