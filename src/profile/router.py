from fastapi import APIRouter, status, Depends, HTTPException
import models
from auth import utils as auth_utils
from sqlalchemy.orm import Session
from database import get_db
from . import schemas
from uuid import UUID

router = APIRouter()

@router.patch('', status_code=status.HTTP_201_CREATED, response_model=schemas.ProfileReturnSchema)
async def update_profile(
    data: schemas.UpdateProfileSchema, 
    db: Session = Depends(get_db),
    payload: dict = Depends(auth_utils.validate_access_token)):

    ## convert user id from payload to UUID
    user_id_from_token = UUID(payload.get('sub'))

    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id_from_token).first()
    if not profile:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Profile does not exist"
        )

    profile.first_name = data.first_name
    profile.last_name = data.last_name
    profile.email = data.email
    profile.role = data.role


    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile

@router.get('/{profile_id}', status_code=status.HTTP_200_OK, response_model=schemas.ProfileReturnSchema)
async def get_profile(
    profile_id: str,
    db: Session = Depends(get_db),
    payload: dict = Depends(auth_utils.validate_access_token)):

    profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Profile does not exist"
        )

    return profile