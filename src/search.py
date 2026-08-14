import re
from collections import Counter


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Фильтрует список банковских операций по строке поиска в описании.
    Регистр символов не учитывается.
    """
    if not search:
        return data

    # Экранируем спецсимволы и компилируем паттерн для быстрого поиска
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    filtered_data = []

    for item in data:
        # Безопасно получаем строку описания (если ключа нет, вернет '')
        description = item.get("description", "")

        # Если находим совпадение, добавляем словарь в результат
        if re.search(pattern, description):
            filtered_data.append(item)

    return filtered_data


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """
    Подсчитывает количество операций для каждой категории из переданного списка.
    Категории ищутся в поле 'description'.
    """
    # Собираем все описания из списка операций
    descriptions = [item.get("description") for item in data if "description" in item]

    # Подсчитываем количество упоминаний каждого описания в данных
    counts = Counter(descriptions)

    # Формируем итоговый словарь только для запрашиваемых категорий
    # Если категории нет в данных, счетчик вернет 0
    result = {category: counts[category] for category in categories}

    return result
