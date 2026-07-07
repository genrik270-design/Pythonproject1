def get_date(date_string: str) -> str:
    """Преобразует дату через срезы строк."""
    # date_string[:10] вернет "2026-06-29"
    year, month, day = date_string[:10].split("-")
    return f"{day}.{month}.{year}"