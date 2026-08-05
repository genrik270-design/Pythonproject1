import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

API_KEY = os.getenv("API_KEY")


def convert_to_rubles(transaction: dict) -> float:
    """Возвращает сумму транзакции в рублях (float).

    Если валюта отличная от RUB (USD или EUR), обращается к API.
    """
    operation_amount = transaction.get("operationAmount", {})
    amount = float(operation_amount.get("amount", 0.0))
    currency = operation_amount.get("currency", {}).get("code", "RUB")

    if currency == "RUB":
        return amount

    if currency in ["USD", "EUR"]:
        url = f"https://apilayer.com{currency}&symbols=RUB"
        headers = {"apikey": API_KEY}

        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()
            rate = data.get("rates", {}).get("RUB", 1.0)
            return float(amount * rate)
        except (requests.RequestException, KeyError, ValueError):
            return 0.0

    return 0.0
