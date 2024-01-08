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
async def create_product():
    pass

@router.get('/{product_id}', status_code=status.HTTP_200_OK )
async def get_product_by_id():
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