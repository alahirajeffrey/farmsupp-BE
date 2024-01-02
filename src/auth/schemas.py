from datetime import datetime
from pydantic import BaseModel, constr, Field

class CreateUserSchema(BaseModel):
    mobile_number: str
    password: constr(min_length=8)
    country_code: str = Field(default="+234")

class UserReturnSchema(BaseModel):
    mobile_number: str
    id: str
    country_code: str
    is_mobile_verified: bool
    created_at: datetime
    updated_at: datetime