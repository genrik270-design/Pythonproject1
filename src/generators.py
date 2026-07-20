from typing import Iterable, Iterator

def filter_transactions_by_currency(transactions: Iterable[dict], currency: str) -> Iterator[dict]:
    """
    Фильтрует транзакции по заданной валюте (например, 'USD', 'RUB').
    Возвращает итератор с транзакциями.
    """
    for transaction in transactions:
        # Проверяем структуру. Если вложенность другая, измените этот путь
        try:
            if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
                yield transaction
        except AttributeError:
            continue


def transaction_descriptions(transactions: Iterable[dict]) -> Iterator[str]:
    """
    Возвращает описание (description) каждой транзакции.
    """
    for transaction in transactions:
        yield transaction.get("description", "Описание отсутствует")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генерирует номера карт в формате 0000 0000 0000 0000 в заданном диапазоне.
    """
    for number in range(start, end + 1):
        # Дополняем нулями до 16 знаков и форматируем по 4 цифры
        card_str = f"{number:016d}"
        yield f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:]}"

        def transaction_descriptions(transactions: Iterable[dict]) -> Iterator[str]:
            """
            Принимает итерируемый объект со словарями транзакций
            и по очереди возвращает описание (description) каждой операции.
            """
            for transaction in transactions:
                # Используем .get(), чтобы избежать ошибки KeyError, если ключа 'description' нет
                yield transaction.get("description", "Описание отсутствует")