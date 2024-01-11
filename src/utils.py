from passlib.context import CryptContext
from typing import Union, Any
from datetime import datetime, timedelta
from config import config
from jose import jwt
from fastapi.security import OAuth2PasswordBearer 
from fastapi import HTTPException, status, Depends
from openai import OpenAI
import logging
import cloudinary

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

## generate response from openai 
async def generate_openai_response(message):
    try:
        client = OpenAI(api_key= config.get("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user", "content": f"{message}"}]
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.exception(e)

## remove new lines from openai response
def remove_newlines(text):
    return text.replace("\n", "")

def upload_image(type, image_path):
    cloudinary.config(
        cloud_name=config.get("CLOUDINARY_CLOUD_NAME"),
        api_key=config.get("CLOUDINARY_API_KEY"),
        api_secret=config.get("CLOUDINARY_API_SECRET")
    )

    try:
        if type == "profile_picture":
            response = cloudinary.uploader.upload_image(
                file= image_path,
                folder="profile/picture/",
            )
            return response
            
        if type == "product_image":
            response = cloudinary.uploader.upload_image(
                file= image_path,
                folder="product/image/",
            )
            return response
        
    except Exception as e:
        logging.error(f"Error uploading image to Cloudinary: {e}")
        return None
    