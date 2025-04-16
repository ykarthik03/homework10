import pytest
from app.dependencies import get_settings, require_role, get_current_user
from fastapi import HTTPException


def test_get_settings_returns_settings():
    settings = get_settings()
    assert hasattr(settings, 'smtp_server')
    assert hasattr(settings, 'smtp_port')


def test_require_role_allows_valid_role():
    checker = require_role(["ADMIN"])
    user = {"user_id": "1", "role": "ADMIN"}
    assert checker(current_user=user) == user


def test_require_role_denies_invalid_role():
    checker = require_role(["ADMIN"])
    user = {"user_id": "1", "role": "USER"}
    with pytest.raises(HTTPException):
        checker(current_user=user)


def test_get_current_user_valid(monkeypatch):
    def fake_decode_token(token):
        return {"sub": "1", "role": "ADMIN"}
    monkeypatch.setattr("app.dependencies.decode_token", fake_decode_token)
    token = "sometoken"
    user = get_current_user(token)
    assert user["user_id"] == "1"
    assert user["role"] == "ADMIN"


def test_get_current_user_invalid(monkeypatch):
    def fake_decode_token(token):
        return None
    monkeypatch.setattr("app.dependencies.decode_token", fake_decode_token)
    token = "sometoken"
    with pytest.raises(HTTPException):
        get_current_user(token)
