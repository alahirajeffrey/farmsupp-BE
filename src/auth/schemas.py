from datetime import datetime
from pydantic import BaseModel, constr, Field, UUID4

class CreateUserSchema(BaseModel):
    mobile_number: str
    password: constr(min_length=8)
    country_code: str = Field(default="+234")

class UserReturnSchema(BaseModel):
    mobile_number: str
    id: UUID4
    country_code: str
    is_mobile_verified: bool
    created_at: datetime
    updated_at: datetime

class LoginSchema(BaseModel):
    mobile_number: str
    password: str

class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str
    
class VerifyMobileSchema(BaseModel):
    otp: str