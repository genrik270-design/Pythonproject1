import os
import logging

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Настраиваем путь к masks.log
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

file_handler = logging.FileHandler(os.path.join(LOG_DIR, "masks.log"), mode='w', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты.

    Формат маски: XXXX XX** **** XXXX
    """
    logger.debug(f"Старт маскирования карты. Входные данные: {card_number[:4]}********")

    if not card_number.isdigit() or len(card_number) != 16:
        # Логируем ошибку, если номер не состоит из 16 цифр
        logger.error(f"Провал: Некорректный номер карты '{card_number}'. Ожидалось 16 цифр.")
        return "Некорректный номер карты"

    masked_card = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"
    logger.debug(f"Успех: Карта замаскирована -> {masked_card}")
    return masked_card


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета.

    Формат маски: **XXXX (только последние 4 цифры)
    """
    logger.debug(f"Старт маскирования счета. Входные данные: ********{account_number[-4:]}")

    if not account_number.isdigit() or len(account_number) < 4:
        # Логируем ошибку, если номер счета некорректен
        logger.error(f"Провал: Некорректный номер счета '{account_number}'. Ожидалось минимум 4 цифры.")
        return "Некорректный номер счета"

    masked_account = f"**{account_number[-4:]}"
    logger.debug(f"Успех: Счет замаскирован -> {masked_account}")
    return masked_account
