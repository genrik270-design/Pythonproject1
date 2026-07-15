import pytest
from src.masks import get_mask_card_number, get_mask_account


# =====================================================================
# ТЕСТЫ ДЛЯ ФУНКЦИИ get_mask_card_number
# =====================================================================

# 1. Проверка правильности маскирования для стандартных 16-значных карт
@pytest.mark.parametrize("card_number, expected", [
    ("7000792289606361", "7000 79** **** 6361"),
    ("1111222233334444", "1111 22** **** 4444"),
])
def test_get_mask_card_number_valid(card_number, expected):
    """Тестирование правильности маскирования для корректных номеров карт."""
    assert get_mask_card_number(card_number) == expected


# 2. Проверка реакции на некорректные форматы и длины (включая 19 знаков)
@pytest.mark.parametrize("invalid_card", [
    "1234567890",              # Слишком короткий
    "abcdefghijklmnop",        # Буквы вместо цифр
    "1234567890123456789",     # 19 знаков (код считает это ошибкой из-за len != 16)
])
def test_get_mask_card_number_invalid_inputs(invalid_card):
    """Проверка возврата строки ошибки при неверном формате или длине."""
    assert get_mask_card_number(invalid_card) == "Некорректный номер карты"


# 3. Проверка отсутствия номера карты или передачи пустых строк
@pytest.mark.parametrize("empty_input", ["", "   "])
def test_get_mask_card_number_missing(empty_input):
    """Проверка, что функция возвращает строку ошибки на пустой ввод."""
    assert get_mask_card_number(empty_input) == "Некорректный номер карты"


# =====================================================================
# ТЕСТЫ ДЛЯ ФУНКЦИИ get_mask_account
# =====================================================================

# 1. Проверка правильности маскирования номеров счетов
@pytest.mark.parametrize("account_number, expected", [
    ("73654108430135874305", "**4305"),  # Стандартный 20-значный счет
    ("1234567890123456", "**3456"),      # 16-значный счет
])
def test_get_mask_account_valid(account_number, expected):
    """Тестирование правильности маскирования номеров счетов разной длины."""
    assert get_mask_account(account_number) == expected


# 2. Проверка счетов, которые короче 4 символов или содержат не-цифры
@pytest.mark.parametrize("invalid_account", [
    "123",        # Меньше 4 символов
    "1",          # 1 символ
    "",           # Пустая строка
    "123a",       # Содержит буквы
])
def test_get_mask_account_invalid_inputs(invalid_account):
    """Проверка возврата строки ошибки при коротком счете или неверном формате."""
    assert get_mask_account(invalid_account) == "Некорректный номер счета"