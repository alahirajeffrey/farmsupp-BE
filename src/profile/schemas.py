from datetime import datetime
from pydantic import BaseModel, UUID4
from enum import Enum

class Role(str, Enum):
    FARMER= "FARMER"
    ADMIN= "ADMIN"
    USER= "USER"

class UpdateProfileSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    role: Role

class ProfileReturnSchema(UpdateProfileSchema):
    created_at: datetime
    updated_at: datetime
    id: UUID4

