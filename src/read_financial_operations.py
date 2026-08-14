import os
from typing import Any

import pandas as pd


def read_csv_financial_operations(file_path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла и возвращает список словарей."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    try:
        df = pd.read_csv(file_path, sep=None, engine="python", encoding="utf-8")
        df.columns = df.columns.str.strip()

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime(
                "%Y-%m-%d %H:%M"
            )
        if "amount" in df.columns:
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

        df = df.dropna(subset=["date", "amount"])
        return df.to_dict(orient="records")
    except (FileNotFoundError, pd.errors.EmptyDataError, ValueError, KeyError) as e:
        print(f"Ошибка при чтении CSV {file_path}: {e}")
        return []


def read_excel_financial_operations(file_path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла (.xlsx/.xls) и возвращает список словарей."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    try:
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime(
                "%Y-%m-%d %H:%M"
            )
        if "amount" in df.columns:
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

        df = df.dropna(subset=["date", "amount"])
        return df.to_dict(orient="records")
    except (FileNotFoundError, pd.errors.EmptyDataError, ValueError, KeyError) as e:
        print(f"Ошибка при чтении Excel {file_path}: {e}")
        return []
