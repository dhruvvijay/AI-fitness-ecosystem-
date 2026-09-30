"""
Security utilities: JWT token management, password hashing, OAuth, and RBAC.
"""

import secrets
import random
import string
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Optional

import jwt
from passlib.context import CryptContext

from app.core.config import settings


# ── Password Hashing ────────────────────────────────────────────

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ── JWT Tokens ───────────────────────────────────────────────────

class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


def create_access_token(
    data: Optional[dict] = None,
    subject: Optional[int] = None,
    role: str = "user",
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create JWT access token. Accepts either a data dict or subject+role."""
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    if data:
        payload = {**data, "exp": expire, "iat": datetime.now(timezone.utc), "jti": secrets.token_urlsafe(32)}
    else:
        payload = {
            "sub": str(subject),
            "role": role,
            "type": TokenType.ACCESS.value,
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "jti": secrets.token_urlsafe(32),
        }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(
    data: Optional[dict] = None,
    subject: Optional[int] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create JWT refresh token. Accepts either a data dict or subject."""
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    if data:
        payload = {**data, "exp": expire, "iat": datetime.now(timezone.utc), "jti": secrets.token_urlsafe(32)}
    else:
        payload = {
            "sub": str(subject),
            "type": TokenType.REFRESH.value,
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "jti": secrets.token_urlsafe(32),
        }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


def create_token_pair(user_id: int, role: str = "user") -> dict[str, str]:
    return {
        "access_token": create_access_token(subject=user_id, role=role),
        "refresh_token": create_refresh_token(subject=user_id),
        "token_type": "bearer",
    }


# ── OTP Generation ──────────────────────────────────────────────

def generate_otp(length: int = 6) -> str:
    return "".join(random.choices(string.digits, k=length))


def generate_reset_token() -> str:
    return secrets.token_urlsafe(64)


# ── Role-Based Access Control ────────────────────────────────────

class UserRole(str, Enum):
    ADMIN = "admin"
    TRAINER = "trainer"
    USER = "user"


ROLE_HIERARCHY = {
    UserRole.ADMIN: 3,
    UserRole.TRAINER: 2,
    UserRole.USER: 1,
}


def check_role_permission(user_role: str, required_role: str) -> bool:
    user_level = ROLE_HIERARCHY.get(UserRole(user_role), 0)
    required_level = ROLE_HIERARCHY.get(UserRole(required_role), 0)
    return user_level >= required_level
