from passlib.context import CryptContext
from typing import Union, Any
from datetime import datetime, timedelta
from config import config
from jose import jwt
from fastapi.security import OAuth2PasswordBearer 
from fastapi import HTTPException, status, Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", scheme_name="JWT")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

## create access token
def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=30)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, config.get("JWT_SECRET"), "HS256")
    return encoded_jwt

## validate access token
def validate_access_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, config.get("JWT_SECRET"), algorithms="HS256")
        sub: str = payload.get("sub")
        if sub is None:
            raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED, 
            detail= "Invalid credentials"
            )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED, 
            detail= "Token expired"
            )
    
    except jwt.JWTError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED, 
            detail= "Could not validate credentials"
            )

    return payload
