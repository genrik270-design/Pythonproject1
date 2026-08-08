import json
import os
import logging
from typing import Any, Dict, List

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Создаем папку в корне
os.makedirs(LOG_DIR, exist_ok=True)
file_handler = logging.FileHandler(
    os.path.join(LOG_DIR, "utils.log"), mode="w", encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)

file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_financial_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Читает JSON-файл и возвращает список словарей с транзакциями.

    Если файл пустой, содержит не список или не найден, возвращает пустой список."""

    logger.debug(f"Старт get_financial_transactions. Файл: {file_path}")

    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                logger.debug(
                    f"Файл {file_path} прочитан, найдено {len(data)} элементов"
                )
                return data
            logger.error(f"Данные в {file_path} не являются списком")
            return []

    except (json.JSONDecodeError, TypeError) as e:
        # JSON поврежден — пишем в ERROR
        logger.error(f"Ошибка обработки JSON в {file_path}. Текст: {e}")
        return []
