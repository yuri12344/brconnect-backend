import unittest
from unittest.mock import patch, Mock
from .models import Company, WppConnectSession
from .clients.wppconnect import WppConnectService
import requests

class TestWppConnectService(unittest.TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Test Company")
        self.session = WppConnectSession.objects.create(company=self.company, whatsapp_api_session="test_session")
        self.service = WppConnectService(self.company, "test_session")

    @patch('requests.post')
    def test_send_message_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        response = self.service.send_message("1234567890", False, "Test message")
        self.assertEqual(response, {"message": "Message sent successfully"})
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_send_message_failure(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
        mock_post.return_value = mock_response

        response = self.service.send_message("1234567890", False, "Test message")
        self.assertIsNone(response)
        mock_post.assert_called_once()

    def test_send_message_no_phone_or_message(self):
        with self.assertRaises(ValueError):
            self.service.send_message("", False, "")
        with self.assertRaises(ValueError):
            self.service.send_message("1234567890", False, "")
        with self.assertRaises(ValueError):
            self.service.send_message("", False, "Test message")

if __name__ == '__main__':
    unittest.main()

