from fastapi import APIRouter, status, Depends, HTTPException, Query
import models
import utils
from sqlalchemy.orm import Session
from database import get_db
from . import schemas
from uuid import UUID

router = APIRouter()

@router.patch('', status_code=status.HTTP_201_CREATED, response_model=schemas.ProfileReturnSchema)
async def update_profile(
    data: schemas.UpdateProfileSchema, 
    db: Session = Depends(get_db),
    payload: dict = Depends(utils.validate_access_token)):

    ## convert user id from payload to UUID
    user_id_from_token = UUID(payload.get('sub'))

    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id_from_token).first()
    if not profile:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Profile does not exist"
        )

    if data.first_name is not None:
        profile.first_name = data.first_name
    if data.last_name is not None:
        profile.last_name = data.last_name
    if data.email is not None:
        profile.email = data.email
    if data.role is not None:
        profile.role = data.role


    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile

@router.get('/other/{profile_id}', status_code=status.HTTP_200_OK, response_model=schemas.ProfileReturnSchema)
async def get_others_profile(
    profile_id: str,
    db: Session = Depends(get_db),
    payload: dict = Depends(utils.validate_access_token)):

    profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Profile does not exist"
        )

    return profile

@router.get('/own', status_code=status.HTTP_200_OK, response_model=schemas.ProfileReturnSchema)
async def get_own_profile(
    db: Session = Depends(get_db),
    payload: dict = Depends(utils.validate_access_token)):

    ## convert user id from payload to UUID
    user_id_from_token = UUID(payload.get('sub'))

    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id_from_token).first()
    if not profile:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Profile does not exist"
        )

    return profile

@router.get('/farmers', status_code=status.HTTP_200_OK)
async def get_farmers_profiles(
    db: Session = Depends(get_db),
    page: int = Query(1, description="Page number", gt=0),
    page_size: int = Query(10, description="Items per page", gt=0, le=100),
    payload: dict = Depends(utils.validate_access_token)):

    offset = (page - 1) * page_size

    profiles = db.query(models.Profile).filter(models.Profile.role == "FARMER").offset(offset).limit(page_size).all()
    if len(profiles) == 0:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "No farmers have registered"
        )
    
    return profiles
    