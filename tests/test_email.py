import pytest
from app.services.email_service import EmailService
from app.utils.template_manager import TemplateManager

from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_send_markdown_email(email_service):
    with patch("app.utils.smtp_connection.SMTPClient.send_email", new_callable=AsyncMock) as mock_send_email:
        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "verification_url": "http://example.com/verify?token=abc123"
        }
        await email_service.send_user_email(user_data, 'email_verification')
        mock_send_email.assert_awaited_once()
    # Manual verification in Mailtrap
