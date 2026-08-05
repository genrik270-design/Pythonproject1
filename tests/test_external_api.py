import unittest
from unittest.mock import Mock, patch
from src.external_api import convert_to_rubles


class TestExternalApi(unittest.TestCase):

    def test_convert_rubles_directly(self):
        """Если транзакция в RUB, API вызываться не должен."""
        transaction = {
            "operationAmount": {"amount": "150.50", "currency": {"code": "RUB"}}
        }
        result = convert_to_rubles(transaction)
        self.assertEqual(result, 150.50)
        self.assertIsInstance(result, float)

    @patch("requests.get")
    def test_convert_usd_with_mock_api(self, mock_get):
        """Тест конвертации USD через Mock-ответ стороннего API."""
        transaction = {
            "operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}
        }

        # Настраиваем фейковый успешный ответ от API со значением курса
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"rates": {"RUB": 75.5}}
        mock_get.return_value = mock_response

        result = convert_to_rubles(transaction)

        # Проверяем математику: 100 * 75.5 = 7550.0
        self.assertEqual(result, 7550.0)


if __name__ == "__main__":
    unittest.main()
