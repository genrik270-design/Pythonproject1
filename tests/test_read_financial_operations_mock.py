from unittest.mock import patch

import pandas as pd

from src.read_financial_operations import (
    read_csv_financial_operations,
    read_excel_financial_operations,
)


@patch("os.path.exists")
@patch("pandas.read_csv")
def test_read_csv_success_mock(mock_read_csv, mock_exists):
    """Тест успешного чтения CSV с использованием mock."""
    mock_exists.return_value = True

    # Имитируем данные, которые возвращает pandas
    fake_df = pd.DataFrame(
        [{"date": "2023-09-05T11:30:32Z", "amount": 16210, "state": "EXECUTED"}]
    )
    mock_read_csv.return_value = fake_df

    result = read_csv_financial_operations("fake_path.csv")

    mock_read_csv.assert_called_once_with(
        "fake_path.csv", sep=None, engine="python", encoding="utf-8"
    )
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["amount"] == 16210


@patch("os.path.exists")
@patch("pandas.read_excel")
def test_read_excel_success_mock(mock_read_excel, mock_exists):
    """Тест успешного чтения Excel с использованием mock."""
    mock_exists.return_value = True

    fake_df = pd.DataFrame(
        [{"date": "2023-09-06T12:00:00Z", "amount": 500, "state": "EXECUTED"}]
    )
    mock_read_excel.return_value = fake_df

    result = read_excel_financial_operations("fake_path.xlsx")

    mock_read_excel.assert_called_once_with("fake_path.xlsx")
    assert isinstance(result, list)
    assert result[0]["amount"] == 500
