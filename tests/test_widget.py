import pytest
from src.widget import mask_account_card, get_date


# =====================================================================
# ТЕСТЫ ДЛЯ ФУНКЦИИ mask_account_card
# =====================================================================

# 1. Проверка правильности распознавания типов карт и счетов
@pytest.mark.parametrize("input_string, expected", [
    ("Visa Gold 7000792289606361", "Visa Gold 7000 79** **** 6361"),
    ("Mastercard 1111222233334444", "Mastercard 1111 22** **** 4444"),
    ("Счет 73654108430135874305", "Счет **4305"),
    ("Счет 1234567890123456", "Счет **3456"),
])
def test_mask_account_card_valid(input_string, expected):
    """Проверка, что функция корректно распознает тип данных и применяет верную маску."""
    assert mask_account_card(input_string) == expected


# 2. Тестирование устойчивости к некорректным входным данным и устойчивости к ошибкам
@pytest.mark.parametrize("invalid_input, expected_error", [
    ("Visa Gold 12345", "Visa Gold Некорректный номер карты"), # Короткий номер карты
    ("Счет 123", "Счет Некорректный номер счета"),             # Короткий номер счета
    ("Visa Gold abcdefghijklmnop", "Visa Gold Некорректный номер карты"), # Буквы в номере
])
def test_mask_account_card_invalid_data(invalid_input, expected_error):
    """Проверка склеивания строк ошибок из модуля masks."""
    assert mask_account_card(invalid_input) == expected_error


# 3. Тестирование граничных случаев (пустые строки и неверная структура)
@pytest.mark.parametrize("edge_input, expected_res", [
    ("", "Передана пустая строка"),
    ("ПростоТекстБезПробелов", "Некорректный формат данных"),
    ("   ", "Некорректный формат данных"), # split() вернет пустой список
])
def test_mask_account_card_edge_cases(edge_input, expected_res):
    """Проверка реакции функции на пустой ввод или отсутствие структуры данных."""
    assert mask_account_card(edge_input) == expected_res


# =====================================================================
# ТЕСТЫ ДЛЯ ФУНКЦИИ get_date
# =====================================================================

# 1. Проверка правильности преобразования валидных ISO-строк
@pytest.mark.parametrize("iso_string, expected_date", [
    ("2026-06-29T10:14:00.000000", "29.06.2026"),
    ("2025-12-31T23:59:59.999999", "31.12.2025"),
    ("2024-01-01T00:00:00.000000", "01.01.2024"),
])
def test_get_date_valid(iso_string, expected_date):
    """Тестирование правильности преобразования даты."""
    assert get_date(iso_string) == expected_date


# 2. Проверка работы функции на различных неверных форматах дат
@pytest.mark.parametrize("invalid_date", [
    "29-06-2026",               # Неверный порядок/разделители
    "invalid-date-format",      # Обычный текст
    "2026/06/29",               # Косая черта вместо дефиса
    "",                         # Пустая строка
    "   ",                      # Строка из пробелов
])
def test_get_date_invalid_formats(invalid_date):
    """Проверка, что функция корректно генерирует ValueError при неверном формате."""
    with pytest.raises(ValueError):
        get_date(invalid_date)


# 3. Проверка поведения при полном отсутствии объекта (передача None)
def test_get_date_none():
    """Проверка, что передача None вызывает ошибку атрибута из-за метода split()."""
    with pytest.raises(AttributeError):
        get_date(None)
