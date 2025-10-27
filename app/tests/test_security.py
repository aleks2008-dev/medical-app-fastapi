import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch
from app.core.test_security import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    create_reset_token, 
    verify_reset_token
)
from fastapi import HTTPException

def test_password_hashing():
    password = "test_password_123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong_password", hashed)

def test_create_access_token():
    data = {"sub": "user123"}
    token = create_access_token(data)
    
    assert isinstance(token, str)
    assert len(token) > 0

def test_create_access_token_with_expiry():
    data = {"sub": "user123"}
    expires_delta = timedelta(minutes=15)
    token = create_access_token(data, expires_delta)
    
    assert isinstance(token, str)
    assert len(token) > 0

def test_create_reset_token():
    email = "test@example.com"
    token = create_reset_token(email)
    
    assert isinstance(token, str)
    assert len(token) > 0

def test_verify_reset_token():
    email = "test@example.com"
    token = create_reset_token(email)
    
    verified_email = verify_reset_token(token)
    assert verified_email == email

def test_verify_invalid_reset_token():
    invalid_token = "invalid.token.here"
    verified_email = verify_reset_token(invalid_token)
    assert verified_email is None

@pytest.mark.asyncio
@patch('app.core.security.token_storage')
async def test_verify_token_blacklisted(mock_token_storage):
    from app.core.security import verify_token
    
    mock_token_storage.is_token_blacklisted = AsyncMock(return_value=True)
    
    with pytest.raises(HTTPException) as exc_info:
        await verify_token("blacklisted_token")
    
    assert exc_info.value.status_code == 401
    assert "revoked" in exc_info.value.detail