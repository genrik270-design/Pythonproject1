import os

from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.read_financial_operations import read_csv_financial_operations, read_excel_financial_operations
from src.search import process_bank_operations, process_bank_search
from src.utils import get_financial_transactions


def format_account_or_card(source: str) -> str:
    """Вспомогательная функция для маскирования отправителя или получателя."""
    if not source:
        return ""

    parts = source.split()
    number = parts[-1]
    name = " ".join(parts[:-1])

    if name.lower() == "счет":
        return f"Счет {get_mask_account(number)}"
    else:
        return f"{name} {get_mask_card_number(number)}"


def main() -> None:
    """Основная логика проекта, связывающая функциональности между собой."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    user_choice = input("Пользователь: ").strip()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    json_path = os.path.join(base_dir, "data", "operations.json")
    csv_path = os.path.join(base_dir, "data", "transactions.csv")
    xlsx_path = os.path.join(base_dir, "data", "transactions.xlsx")
    # Выбор файла
    try:
        if user_choice == "1":
            print("\nПрограмма: Для обработки выбран JSON-файл.")
            transactions = get_financial_transactions(json_path)
        elif user_choice == "2":
            print("\nПрограмма: Для обработки выбран CSV-файл.")
            transactions = read_csv_financial_operations(csv_path)
        elif user_choice == "3":
            print("\nПрограмма: Для обработки выбран XLSX-файл.")
            transactions = read_excel_financial_operations(xlsx_path)
        else:
            print("\nПрограмма: Неверный пункт меню. Завершение программы.")
            return
    except FileNotFoundError:
        print("\nПрограмма: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # 1. Фильтрация по статусу
    print("\nПрограмма: Выберите статус интересующих вас операций:")
    print("Доступные статусы: EXECUTED, CANCELED, PENDING")
    status_choice = input("Пользователь: ").strip().upper()

    if status_choice in ["EXECUTED", "CANCELED", "PENDING"]:
        print(f"\nПрограмма: Операции отфильтрованы по статусу {status_choice}")
        transactions = filter_by_state(transactions, status_choice)
    else:
        print(f"\nПрограмма: Статус '{status_choice}' не существует. Вывод всех операций.")

    # 2. Сортировка по дате
    print("\nПрограмма: Отсортировать операции по дате? Да/Нет")
    sort_choice = input("Пользователь: ").strip().lower()

    if sort_choice == "да":
        print("\nПрограмма: Отсортировать по возрастанию или по убыванию?")
        order_choice = input("Пользователь: ").strip().lower()

        if "возраст" in order_choice:
            transactions = sort_by_date(transactions, reverse=False)
        else:
            transactions = sort_by_date(transactions, reverse=True)

    # 3. Фильтрация по валюте (только рубли)
    print("\nПрограмма: Выводить только рублевые транзакции? Да/Нет")
    rub_choice = input("Пользователь: ").strip().lower()

    if rub_choice == "да":
        filtered_rub = []
        for t in transactions:
            currency_code_json = t.get("operationAmount", {}).get("currency", {}).get("code")
            currency_name_json = t.get("operationAmount", {}).get("currency", {}).get("name")
            currency_code_csv = t.get("currency_code")

            if "RUB" in [currency_code_json, currency_code_csv] or "руб." in [currency_name_json]:
                filtered_rub.append(t)
        transactions = filtered_rub

    # 4. Фильтрация по ключевому слову в описании
    print("\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    word_filter_choice = input("Пользователь: ").strip().lower()

    if word_filter_choice == "да":
        search_word = input("Пользователь (введите слово для поиска): ").strip()
        transactions = process_bank_search(transactions, search_word)

    all_categories = list(set([t.get("description", "") for t in transactions if "description" in t]))
    process_bank_operations(transactions, all_categories)

    # 5. Вывод результатов
    print("\nПрограмма: Распечатываю итоговый список транзакций...\n")

    if not transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Программа: \nВсего банковских операций в выборке: {len(transactions)}\n")

    for t in transactions:
        raw_date = t.get("date", "")
        formatted_date = ""
        if raw_date and len(raw_date) >= 10:
            if "-" in raw_date[:10]:
                year, month, day = raw_date[:10].split("-")
                formatted_date = f"{day}.{month}.{year}"
            elif "." in raw_date[:10]:
                formatted_date = raw_date[:10]

        description = t.get("description", "Без описания")

        from_info = format_account_or_card(t.get("from", ""))
        to_info = format_account_or_card(t.get("to", ""))

        if from_info:
            transfer_route = f"{from_info} -> {to_info}"
        else:
            transfer_route = to_info

        amount = t.get("amount") or t.get("operationAmount", {}).get("amount", "0")

        currency = t.get("currency_code") or t.get("operationAmount", {}).get("currency", {}).get("name", "")
        if currency == "RUB":
            currency = "руб."

        print(f"{formatted_date} {description}")
        if transfer_route:
            print(transfer_route)
        print(f"Сумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
