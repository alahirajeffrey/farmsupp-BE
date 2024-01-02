from fastapi import APIRouter, status, Depends, HTTPException
from auth.schemas import CreateUserSchema, UserReturnSchema
from sqlalchemy.orm import Session
from database import get_db
from auth import models, utils

router = APIRouter()

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserReturnSchema)
def register_user(data: CreateUserSchema, db: Session = Depends(get_db)):
    
    ## check if user exists
    user_exists = db.query(models.User).filter(models.User.mobile_number == data.mobile_number).first()
    if user_exists:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "User with mobile number already exists"
        )
    
    ## create user
    new_user = models.User(
        mobile_number= data.mobile_number,
        password= utils.hash_password(data.password),
        country_code= data.country_code
    )

    db.add(new_user)
    db.commit()
    db.refresh()


    return new_user

@router.post('/login', status_code=status.HTTP_200_OK)
def login():
    return {"message":"user signed in"}

@router.patch('/change-password', status_code=status.HTTP_200_OK)
def change_password():
    return {"message":"Change password"}

@router.post('/request-password-reset', status_code=status.HTTP_200_OK)
def request_password_reset():
    return {"message":"Password reset link sent"}

@router.patch('/reset-password', status_code=status.HTTP_200_OK)
def reset_password():
    return {"message":"Reset password"}

@router.post('/request-mobile-verification', status_code=status.HTTP_200_OK)
def request_mobile_verification():
    return {"message":"Mobile verification otp sent"}

@router.patch('/verify-mobile', status_code=status.HTTP_200_OK)
def verify_mobile():
    return {"message":"Verify mobile"}