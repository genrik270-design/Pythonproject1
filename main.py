# Импортируем функцию из папки src из файла utils
from src.utils import get_financial_transactions


def main():
    # Укажите путь к вашему JSON-файлу с транзакциями
    path_to_json = "data/operations.json"

    print("Запуск программы...")
    transactions = get_financial_transactions(path_to_json)
    print(f"Завершено. Результат передан в логи. Найдено транзакций: {len(transactions)}")

if __name__ == "__main__":
    main()


from src.masks import get_mask_account, get_mask_card_number

# Внутри функции main():
get_mask_card_number("1234567812345678")  # Успех
get_mask_card_number("1234")              # Ошибка для проверки лога ERROR
get_mask_account("7365472654372654")      # Успех
