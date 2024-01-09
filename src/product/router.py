from fastapi import APIRouter, status, Depends, HTTPException, Query
from product import schemas
from database import get_db
import models
from sqlalchemy.orm import Session
from auth import utils as auth_utils
from uuid import UUID
from profile.schemas import Role

router = APIRouter()

@router.post('', status_code=status.HTTP_201_CREATED )
async def create_product(
    data: schemas.CreateProductSchema,
    db: Session = Depends(get_db),
    payload: dict = Depends(auth_utils.validate_access_token)):

    ## convert user id from payload to UUID
    user_id_from_token = UUID(payload.get('sub'))
    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id_from_token).first()

    if profile is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Profile does not exist"
        )

    if profile.role != Role.FARMER:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Only farmers can post articles"
        )
    
    new_product = models.Product(
        profile_id= profile.id,
        name= data.name,
        description= data.description,
        price= data.price,
        quantity= data.quantity,
        unit= data.unit
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@router.get('/{product_id}', status_code=status.HTTP_200_OK )
async def get_product_by_id():
    pass

@router.get('/name/{name}', status_code=status.HTTP_200_OK )
async def get_products_by_name():
    pass

@router.patch('/upload/images', status_code=status.HTTP_200_OK )
async def upload_product_images():
    pass

@router.get('/farmer/{profile_id}', status_code=status.HTTP_200_OK )
async def get_products_by_famer_id():
    pass

@router.patch('/{product_id}', status_code=status.HTTP_200_OK )
async def update_product():
    pass

@router.delete('/{product_id}', status_code=status.HTTP_200_OK )
async def delete_product_by_id():
    pass

