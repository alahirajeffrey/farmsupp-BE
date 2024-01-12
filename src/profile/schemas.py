from datetime import datetime
from pydantic import BaseModel, UUID4
from enum import Enum
from typing import Optional

class Role(str, Enum):
    FARMER= "FARMER"
    ADMIN= "ADMIN"
    USER= "USER"

class UpdateProfileSchema(BaseModel):
    first_name: Optional[str] = None 
    last_name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[Role] = None

class ProfileReturnSchema(UpdateProfileSchema):
    created_at: datetime
    updated_at: datetime
    id: UUID4

