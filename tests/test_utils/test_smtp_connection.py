import pytest
from unittest.mock import patch, MagicMock
from app.utils.smtp_connection import SMTPClient

def test_send_email_success():
    smtp = SMTPClient('smtp.example.com', 587, 'user', 'pass')
    with patch('smtplib.SMTP') as smtp_mock:
        smtp_instance = smtp_mock.return_value.__enter__.return_value
        smtp_instance.sendmail = MagicMock()
        smtp.send_email('Subject', '<html>test</html>', 'to@example.com')
        smtp_instance.sendmail.assert_called_once()

def test_send_email_failure():
    smtp = SMTPClient('smtp.example.com', 587, 'user', 'pass')
    with patch('smtplib.SMTP', side_effect=Exception('fail')):
        with pytest.raises(Exception):
            smtp.send_email('Subject', '<html>test</html>', 'to@example.com')
