from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional

class CreateProductSchema(BaseModel):
    name: str
    description: str
    price: int
    quantity: int
    unit: str
    profile_id: str

class ProductReturnSchema(CreateProductSchema):
    created_at: datetime
    updated_at: datetime
    id: UUID4

class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None