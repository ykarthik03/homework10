import pytest
from app.utils.common import settings

def test_settings_has_expected_attributes():
    # Check for a few expected attributes, adjust as needed for your Settings
    assert hasattr(settings, 'smtp_server')
    assert hasattr(settings, 'smtp_port')
    assert hasattr(settings, 'smtp_username')
    assert hasattr(settings, 'smtp_password')

def test_settings_is_not_none():
    assert settings is not None
