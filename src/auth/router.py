from fastapi import APIRouter, status, Depends, HTTPException
from auth import schemas
from sqlalchemy.orm import Session
from database import get_db
# from src import 
import utils
import models

router = APIRouter()

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model= schemas.UserReturnSchema)
async def register_user(data: schemas.CreateUserSchema, db: Session = Depends(get_db)):
    
    ## check if user exists
    user_exists = db.query(models.User).filter(models.User.mobile_number == data.mobile_number).first()
    if user_exists:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "User with mobile number already exists"
        )
    
    new_user = models.User(
        mobile_number= data.mobile_number,
        password= utils.hash_password(data.password),
        country_code= data.country_code
    )

    db.add(new_user)
    db.commit()

    new_profile = models.Profile(
        mobile_number = data.mobile_number, 
        user_id= new_user.id  
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_user)


    return new_user

@router.post('/login', status_code=status.HTTP_200_OK)
async def login(data: schemas.LoginSchema, db: Session = Depends(get_db)):
    
    ## check if user exists
    user_exists = db.query(models.User).filter(models.User.mobile_number == data.mobile_number).first()
    if not user_exists:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "User does not exist"
        )
    
    # profile = db.query(models.Profile).filter(models.Profile.user_id == user_exists.id).first()
    
    ## verify password
    if not utils.verify_password(data.password, user_exists.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    # payload = {
    #     "sub": user_exists.id,
    #     "mobile_number": user_exists.mobile_number,
    #     "profile_id": profile.id
    # }

    access_token = utils.create_access_token(user_exists.id)

    return { "access_token": access_token }

@router.patch('/change-password', status_code=status.HTTP_200_OK)
async def change_password(
    data: schemas.ChangePasswordSchema, 
    db: Session = Depends(get_db), 
    payload: dict = Depends(utils.validate_access_token)):

    user_exists = db.query(models.User).filter(models.User.id == payload.get('sub')).first()
    if(user_exists is None):
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "User does not exist"
        )
    
    ## verify password
    if not utils.verify_password(data.old_password, user_exists.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    db.query(models.User).filter(models.User.id == payload.get('sub')).update({"password": utils.hash_password(data.new_password)})
    db.commit()

    return {"message": "Password changed successfully" }

@router.post('/request-mobile-verification', status_code=status.HTTP_200_OK)
async def request_mobile_verification(
    db: Session = Depends(get_db), 
    payload: dict = Depends(utils.validate_access_token)
    ):

    user = db.query(models.User).filter(models.User.id == payload.get('sub')).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    
    db.query(models.Otp).filter(models.Otp.user_id == user.id).delete()
    db.commit()
    
    otp = utils.generate_otp()
    
    formatted_mobile_number = f"{user.country_code}" + f"{user.mobile_number}"
    utils.send_message(formatted_mobile_number, f"Your mobile verification otp is {otp}")

    ## sign otp for 10 minutes
    token = utils.create_access_token(otp, 10)

    new_otp = models.Otp(
        token = token,
        user_id = user.id
    )

    db.add(new_otp)
    db.commit()
    
    return {"message": "Mobile verification otp sent"}

@router.patch('/verify-mobile', status_code=status.HTTP_200_OK)
async def verify_mobile(
    data: schemas.VerifyMobileSchema,
    db: Session = Depends(get_db), 
    payload: dict = Depends(utils.validate_access_token)
):
    
    user = db.query(models.User).filter(models.User.id == payload.get('sub')).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    
    token = db.query(models.Otp).filter(models.Otp.user_id == user.id).first()
    decoded_token = utils.validate_access_token(token)
    
    if decoded_token.get("sub") != data.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Otp"
        )

    user.is_mobile_verified = True

    db.commit()   
    
    return {"message":"Mobile number verified"}

@router.post('/request-password-reset', status_code=status.HTTP_200_OK)
async def request_password_reset(
    db: Session = Depends(get_db), 
    payload: dict = Depends(utils.validate_access_token)):


    return {"message":"Password reset link sent"}

@router.patch('/reset-password', status_code=status.HTTP_200_OK)
async def reset_password():
    return {"message":"Reset password"}