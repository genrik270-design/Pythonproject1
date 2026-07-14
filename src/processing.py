from datetime import datetime


def filter_by_state(data: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """Фильтрует список словарей по значению ключа 'state'."""
    filtered_data = []

    for item in data:
        if item.get('state') == state:
            filtered_data.append(item)

    return filtered_data


def sort_by_date(data: list[dict], reverse: bool = True) -> list[dict]:
    """Сортирует список словарей по ключу 'date'.

    Предварительно преобразует строковое значение даты в объект datetime.
    По умолчанию сортировка идет по убыванию (от самых свежих к более старым).
    """

    def get_date_key(item: dict) -> datetime:
        date_str = item.get("date")

        # Если ключа нет или он пустой, возвращаем минимально возможную дату
        if not date_str:
            return datetime.min

        # Заменяем символ 'Z' на смещение +00:00 для стабильной работы парсера
        cleaned_date = str(date_str).replace("Z", "+00:00")

        try:
            return datetime.fromisoformat(cleaned_date)
        except ValueError:
            # На случай, если строка имеет некорректный формат даты
            return datetime.min

    return sorted(data, key=get_date_key, reverse=reverse)
