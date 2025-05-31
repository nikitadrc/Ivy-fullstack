from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .database import get_db
from .models import User, OAuth2Account
from .schemas import TokenData
from .config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = await get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

# OAuth2 providers
async def authenticate_google(
    db: Session,
    token: str
) -> Optional[User]:
    try:
        # Verify Google token and get user info
        google_user = verify_google_token(token)
        if not google_user:
            return None
        
        # Check if OAuth2 account exists
        oauth_account = db.query(OAuth2Account).filter(
            OAuth2Account.provider == "google",
            OAuth2Account.provider_user_id == google_user["sub"]
        ).first()
        
        if oauth_account:
            return oauth_account.user
        
        # Create new user if not exists
        user = await get_user_by_email(db, google_user["email"])
        if not user:
            user = User(
                email=google_user["email"],
                full_name=google_user["name"],
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create OAuth2 account
        oauth_account = OAuth2Account(
            user_id=user.id,
            provider="google",
            provider_user_id=google_user["sub"],
            access_token=token
        )
        db.add(oauth_account)
        db.commit()
        
        return user
    except Exception as e:
        print(f"Google authentication error: {e}")
        return None

async def authenticate_github(
    db: Session,
    code: str
) -> Optional[User]:
    try:
        # Exchange code for access token
        access_token = exchange_github_code(code)
        if not access_token:
            return None
        
        # Get GitHub user info
        github_user = get_github_user(access_token)
        if not github_user:
            return None
        
        # Check if OAuth2 account exists
        oauth_account = db.query(OAuth2Account).filter(
            OAuth2Account.provider == "github",
            OAuth2Account.provider_user_id == str(github_user["id"])
        ).first()
        
        if oauth_account:
            return oauth_account.user
        
        # Create new user if not exists
        user = await get_user_by_email(db, github_user["email"])
        if not user:
            user = User(
                email=github_user["email"],
                full_name=github_user["name"] or github_user["login"],
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create OAuth2 account
        oauth_account = OAuth2Account(
            user_id=user.id,
            provider="github",
            provider_user_id=str(github_user["id"]),
            access_token=access_token
        )
        db.add(oauth_account)
        db.commit()
        
        return user
    except Exception as e:
        print(f"GitHub authentication error: {e}")
        return None

# Helper functions for OAuth2 providers
def verify_google_token(token: str) -> Optional[dict]:
    # Implement Google token verification
    pass

def exchange_github_code(code: str) -> Optional[str]:
    # Implement GitHub code exchange
    pass

def get_github_user(access_token: str) -> Optional[dict]:
    # Implement GitHub user info retrieval
    pass

async def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first() 