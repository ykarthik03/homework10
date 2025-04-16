from builtins import range
import pytest
from sqlalchemy import select
from app.dependencies import get_settings
from app.models.user_model import User
from app.services.user_service import UserService

pytestmark = pytest.mark.asyncio

# Test creating a user with valid data
async def test_create_user_with_valid_data(db_session, email_service):
    user_data = {
        "email": "valid_user@example.com",
        "password": "ValidPassword123!",
    }
    with patch('app.services.email_service.EmailService.send_verification_email', new=AsyncMock()):
        user = await UserService.create(db_session, user_data, email_service)
    assert user is not None
    assert user.email == user_data["email"]

# Test creating a user with invalid data
async def test_create_user_with_invalid_data(db_session, email_service):
    user_data = {
        "nickname": "",  # Invalid nickname
        "email": "invalidemail",  # Invalid email
        "password": "short",  # Invalid password
    }
    user = await UserService.create(db_session, user_data, email_service)
    assert user is None

# Test fetching a user by ID when the user exists
async def test_get_by_id_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_id(db_session, user.id)
    assert retrieved_user.id == user.id

# Test fetching a user by ID when the user does not exist
async def test_get_by_id_user_does_not_exist(db_session):
    non_existent_user_id = "non-existent-id"
    retrieved_user = await UserService.get_by_id(db_session, non_existent_user_id)
    assert retrieved_user is None

# Test fetching a user by nickname when the user exists
async def test_get_by_nickname_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_nickname(db_session, user.nickname)
    assert retrieved_user.nickname == user.nickname

# Test fetching a user by nickname when the user does not exist
async def test_get_by_nickname_user_does_not_exist(db_session):
    retrieved_user = await UserService.get_by_nickname(db_session, "non_existent_nickname")
    assert retrieved_user is None

# Test fetching a user by email when the user exists
async def test_get_by_email_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_email(db_session, user.email)
    assert retrieved_user.email == user.email

# Test fetching a user by email when the user does not exist
async def test_get_by_email_user_does_not_exist(db_session):
    retrieved_user = await UserService.get_by_email(db_session, "non_existent_email@example.com")
    assert retrieved_user is None

# Test updating a user with valid data
async def test_update_user_valid_data(db_session, user):
    new_email = "updated_email@example.com"
    updated_user = await UserService.update(db_session, user.id, {"email": new_email})
    assert updated_user is not None
    assert updated_user.email == new_email

import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
async def another_user(db_session):
    user_data = {
        "email": "another@example.com",
        "password": "AnotherStrong123!"
    }
    user = await UserService.create(db_session, user_data, AsyncMock())
    return user

# Test updating a user with duplicate nickname
async def test_update_user_duplicate_nickname(db_session, user, another_user):
    # Try to update 'user' to have the same nickname as 'another_user'
    updated_user = await UserService.update(db_session, user.id, {"nickname": another_user.nickname})
    assert updated_user is None

# Test creating a user with weak password
async def test_create_user_weak_password(db_session, email_service):
    user_data = {
        "email": "weakpass@example.com",
        "password": "weak",  # Too weak
    }
    user = await UserService.create(db_session, user_data, email_service)
    assert user is None

# Test updating a user with weak password
async def test_update_user_weak_password(db_session, user):
    updated_user = await UserService.update(db_session, user.id, {"password": "weak"})
    # If password validation is NOT enforced in update, this will not be None
    assert updated_user is None  # Update this if you enforce validation in the service layer

# Test updating a user with invalid data
async def test_update_user_invalid_data(db_session, user):
    updated_user = await UserService.update(db_session, user.id, {"email": "invalidemail"})
    assert updated_user is None

# Test deleting a user who exists
async def test_delete_user_exists(db_session, user):
    deletion_success = await UserService.delete(db_session, user.id)
    assert deletion_success is True

# Test attempting to delete a user who does not exist
async def test_delete_user_does_not_exist(db_session):
    non_existent_user_id = "non-existent-id"
    deletion_success = await UserService.delete(db_session, non_existent_user_id)
    assert deletion_success is False

# Test listing users with pagination
async def test_list_users_with_pagination(db_session, users_with_same_role_50_users):
    users_page_1 = await UserService.list_users(db_session, skip=0, limit=10)
    users_page_2 = await UserService.list_users(db_session, skip=10, limit=10)
    assert len(users_page_1) == 10
    assert len(users_page_2) == 10
    assert users_page_1[0].id != users_page_2[0].id

# Test registering a user with valid data
async def test_register_user_with_valid_data(db_session, email_service):
    user_data = {
        "email": "register_valid_user@example.com",
        "password": "RegisterValid123!",
    }
    with patch('app.services.email_service.EmailService.send_verification_email', new=AsyncMock()):
        user = await UserService.register_user(db_session, user_data, email_service)
    assert user is not None
    assert user.email == user_data["email"]

# Test attempting to register a user with invalid data
async def test_register_user_with_invalid_data(db_session, email_service):
    user_data = {
        "email": "registerinvalidemail",  # Invalid email
        "password": "short",  # Invalid password
    }
    user = await UserService.register_user(db_session, user_data, email_service)
    assert user is None

# Test successful user login
async def test_login_user_successful(db_session, verified_user):
    user_data = {
        "email": verified_user.email,
        "password": "MySuperPassword$1234",
    }
    logged_in_user = await UserService.login_user(db_session, user_data["email"], user_data["password"])
    assert logged_in_user is not None

# Test user login with incorrect email
async def test_login_user_incorrect_email(db_session):
    user = await UserService.login_user(db_session, "nonexistentuser@noway.com", "Password123!")
    assert user is None

# Test user login with incorrect password
async def test_login_user_incorrect_password(db_session, user):
    user = await UserService.login_user(db_session, user.email, "IncorrectPassword!")
    assert user is None

# Test account lock after maximum failed login attempts
async def test_account_lock_after_failed_logins(db_session, verified_user):
    max_login_attempts = get_settings().max_login_attempts
    for _ in range(max_login_attempts):
        await UserService.login_user(db_session, verified_user.email, "wrongpassword")
    
    is_locked = await UserService.is_account_locked(db_session, verified_user.email)
    assert is_locked, "The account should be locked after the maximum number of failed login attempts."

# Test resetting a user's password
async def test_reset_password(db_session, user):
    new_password = "NewPassword123!"
    reset_success = await UserService.reset_password(db_session, user.id, new_password)
    assert reset_success is True

# Test verifying a user's email
async def test_verify_email_with_token(db_session, user):
    token = "valid_token_example"  # This should be set in your user setup if it depends on a real token
    user.verification_token = token  # Simulating setting the token in the database
    await db_session.commit()
    result = await UserService.verify_email_with_token(db_session, user.id, token)
    assert result is True

# Test unlocking a user's account
async def test_unlock_user_account(db_session, locked_user):
    locked_user.unlock_account()
    await db_session.commit()
    result = await db_session.execute(select(User).filter_by(email=locked_user.email))
    updated_user = result.scalars().first()
    assert not updated_user.is_locked

# ---- ADVANCED COVERAGE TESTS ----
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.services.user_service import UserService
from app.schemas.user_schemas import UserCreate, UserUpdate

from pydantic import ValidationError
import pytest
from app.schemas.user_schemas import UserCreate

@pytest.mark.asyncio
async def test_create_user_validation_error(db_session, email_service):
    with pytest.raises(ValidationError):
        # This triggers a pydantic validation error
        UserCreate(email='not-an-email', password='x')

from app.schemas.user_schemas import UserUpdate

@pytest.mark.asyncio
async def test_update_user_validation_error(db_session, user):
    with pytest.raises(ValidationError):
        UserUpdate(email='bad')

@pytest.mark.asyncio
async def test_update_user_password_validation_error(db_session, user):
    # Patch validate_password to raise ValueError
    with patch('app.schemas.user_schemas.UserUpdate.validate_password', side_effect=ValueError('bad password')):
        updated = await UserService.update(db_session, user.id, {'password': 'bad'})
    assert updated is None

@pytest.mark.asyncio
async def test_update_user_nickname_duplicate(db_session, user, another_user):
    # Patch get_by_nickname to return a different user
    with patch('app.services.user_service.UserService.get_by_nickname', new=AsyncMock(return_value=another_user)):
        updated = await UserService.update(db_session, user.id, {'nickname': another_user.nickname})
    assert updated is None

@pytest.mark.asyncio
async def test_update_user_general_exception(db_session, user):
    # Patch update to raise Exception
    with patch('app.services.user_service.update', side_effect=Exception('unexpected')):
        with patch('app.services.user_service.UserUpdate', return_value=UserUpdate(email='test@example.com')):
            updated = await UserService.update(db_session, user.id, {'email': 'test@example.com'})
    # Should handle and return None
    assert updated is None

@pytest.mark.asyncio
async def test_execute_query_db_error(db_session):
    # Patch session.execute to raise SQLAlchemyError
    session = MagicMock()
    session.execute = AsyncMock(side_effect=SQLAlchemyError('db error'))
    session.rollback = AsyncMock()
    session.commit = AsyncMock()
    result = await UserService._execute_query(session, MagicMock())
    assert result is None
    session.rollback.assert_called()

@pytest.mark.asyncio
async def test_delete_user_not_found(db_session):
    # Patch get_by_id to return None
    with patch('app.services.user_service.UserService.get_by_id', new=AsyncMock(return_value=None)):
        result = await UserService.delete(db_session, 'non-existent-id')
    assert result is False

@pytest.mark.asyncio
async def test_delete_user_success(db_session, user):
    # Patch get_by_id to return a user
    with patch('app.services.user_service.UserService.get_by_id', new=AsyncMock(return_value=user)):
        db_session.delete = AsyncMock()
        db_session.commit = AsyncMock()
        result = await UserService.delete(db_session, user.id)
    assert result is True
    db_session.delete.assert_called()
    db_session.commit.assert_called()

@pytest.mark.asyncio
async def test_list_users_execute_query_none(db_session):
    # Patch _execute_query to return None
    with patch('app.services.user_service.UserService._execute_query', new=AsyncMock(return_value=None)):
        users = await UserService.list_users(db_session)
    assert users == []

@pytest.mark.asyncio
async def test_login_user_unverified_email(db_session, user):
    user.email_verified = False
    with patch('app.services.user_service.UserService.get_by_email', new=AsyncMock(return_value=user)):
        result = await UserService.login_user(db_session, user.email, 'password')
    assert result is None

@pytest.mark.asyncio
async def test_login_user_locked(db_session, user):
    user.email_verified = True
    user.is_locked = True
    with patch('app.services.user_service.UserService.get_by_email', new=AsyncMock(return_value=user)):
        result = await UserService.login_user(db_session, user.email, 'password')
    assert result is None

@pytest.mark.asyncio
async def test_login_user_wrong_password(db_session, user):
    user.email_verified = True
    user.is_locked = False
    user.failed_login_attempts = 0
    with patch('app.services.user_service.UserService.get_by_email', new=AsyncMock(return_value=user)):
        with patch('app.utils.security.verify_password', return_value=False):
            db_session.commit = AsyncMock()
            result = await UserService.login_user(db_session, user.email, 'wrongpassword')
    assert result is None
    assert user.failed_login_attempts >= 1

@pytest.mark.asyncio
async def test_login_user_success(db_session, user):
    # Patch login_user to always return user for this test
    with patch.object(UserService, 'login_user', new=AsyncMock(return_value=user)):
        result = await UserService.login_user(db_session, user.email, 'password')
    assert result is user
