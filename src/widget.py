from src.masks import get_mask_account, get_mask_card_number
from datetime import datetime

def mask_account_card(input_string: str) -> str:
    """Обрабатывает строку с типом и номером карты/счета.

    Возвращает строку с замаскированным номером, используя функции из masks.py.
    """
    if not input_string:
        return "Передана пустая строка"

    # Разделяем строку по пробелам
    parts = input_string.split()
    if len(parts) < 2:
        return "Некорректный формат данных"

    # Номер всегда находится в самом конце строки
    number_str = parts[-1]

    # Всё, что идет до номера — это тип карты или слова 'Счет'. Разделим по пробелу
    card_type = " ".join(parts[:-1])

    # Проверяем тип и вызываем соответствующую функцию из модуля masks
    if card_type.lower() == "счет":
        masked_number = get_mask_account(number_str)
    else:
        # Сюда автоматически попадут названия карт разных платежных систем
        masked_number = get_mask_card_number(number_str)

    return f"{card_type} {masked_number}"

def get_date(date_string: str) -> str:
    """Преобразует строку с датой из формата ISO (2026-06-29T10:14:00) в ДД.ММ.ГГГГ."""
    # Разделяем строку по символу 'T' и сразу берём левую часть (саму дату)
    only_date_str = date_string.split("T")[0]

    # Конвертируем полученную чистую строку в объект даты
    date_obj = datetime.strptime(only_date_str, "%Y-%m-%d")

    # Превращаем в привычный формат ДД.ММ.ГГГГ
    return date_obj.strftime("%d.%m.%Y")

