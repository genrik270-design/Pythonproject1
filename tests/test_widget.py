import pytest
from src.widget import get_date


def test_get_date_valid():
    """Тест успешного преобразования корректной ISO-строки."""
    assert get_date("2026-06-29T10:14:00.000000") == "29.06.2026"
    assert get_date("2025-12-31T23:59:59.999999") == "31.12.2025"


def test_get_date_invalid_format():
    """Тест на то, что функция корректно падает при неверном формате."""
    with pytest.raises(ValueError):
        get_date("invalid-date-format")