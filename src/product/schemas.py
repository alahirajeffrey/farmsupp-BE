from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional

class CreateProductSchema(BaseModel):
    title: str
    description: str
    price: int
    quantity: int
    unit: str
    name_of_farmer: str

class ProductReturnSchema(CreateProductSchema):
    created_at: datetime
    updated_at: datetime
    id: UUID4

class ProductUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None