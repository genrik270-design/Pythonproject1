def filter_by_state(data: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """Фильтрует список словарей по значению ключа 'state'."""
    filtered_data = []

    for item in data:
        if item.get('state') == state:
            filtered_data.append(item)

    return filtered_data


def sort_by_date(data: list[dict], reverse: bool = True) -> list[dict]:
    """Сортирует список словарей по ключу 'date'.

    По умолчанию сортировка идет по убыванию (от самых свежих к более старым).
    """
    return sorted(data, key=lambda item: item.get('date', ''), reverse=reverse)