from datetime import datetime, timedelta
from typing import Optional
import uuid
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..config.database import SessionLocal
from ..models.user import User
from ..config.settings import settings


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme for API docs
security = HTTPBearer()


class AuthService:
    SECRET_KEY = settings.secret_key or "your-secret-key-change-in-production"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password using bcrypt"""
        return pwd_context.hash(password)

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Optional[timedelta] = None):
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire, "sub": str(uuid.uuid4())})
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt

    @classmethod
    def verify_token(cls, token: str) -> Optional[dict]:
        """Verify a JWT token and return the payload if valid"""
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except JWTError:
            return None

    @classmethod
    def get_current_user(cls, token: str = Depends(security)) -> User:
        """Get the current user from the token in a dependency"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Extract the token from credentials
            token_data = token.credentials
            payload = jwt.decode(token_data, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        # In a real implementation, you'd fetch the user from the database
        # For now, we'll just return a placeholder
        # db = SessionLocal()
        # try:
        #     user = db.query(User).filter(User.email == email).first()
        #     if user is None:
        #         raise credentials_exception
        #     return user
        # finally:
        #     db.close()

        # Placeholder - in a real implementation, fetch user from DB
        return User(email=email, name="Test User", role="student")


# Dependency to get current user
def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Dependency to get the current user from the token"""
    auth_service = AuthService()
    return auth_service.get_current_user(token)


# Function to create a new user with hashed password
def create_user(db: Session, email: str, name: str, password: str, role: str = "student"):
    """Create a new user with hashed password"""
    hashed_password = pwd_context.hash(password)
    db_user = User(
        email=email,
        name=name,
        role=role,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user