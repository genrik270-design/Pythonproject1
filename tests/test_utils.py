import unittest
from unittest.mock import mock_open, patch

from src.utils import get_financial_transactions


class TestUtils(unittest.TestCase):

    @patch("os.path.exists")
    def test_file_not_found(self, mock_exists):
        """Если файл не найден, должен вернуться пустой список."""
        mock_exists.return_value = False
        result = get_financial_transactions("data/operations.json")
        self.assertEqual(result, [])

    @patch("os.path.exists")
    def test_valid_json_list(self, mock_exists):
        """Если файл валидный и содержит список, возвращаем его."""
        mock_exists.return_value = True
        mock_data = '[{"id": 1, "state": "EXECUTED"}]'

        with patch("builtins.open", mock_open(read_data=mock_data)):
            result = get_financial_transactions("data/operations.json")
            self.assertEqual(result, [{"id": 1, "state": "EXECUTED"}])

    @patch("os.path.exists")
    def test_invalid_json_structure(self, mock_exists):
        """Если файл содержит словарь вместо списка — возвращаем пустой список."""
        mock_exists.return_value = True
        mock_data = '{"status": "error"}'

        with patch("builtins.open", mock_open(read_data=mock_data)):
            result = get_financial_transactions("data/operations.json")
            self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
