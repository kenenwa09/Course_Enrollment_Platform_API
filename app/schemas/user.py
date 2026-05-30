from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Literal


class UserBase(BaseModel):
    name: str = Field(...,min_length=2, max_length=50)
    email: EmailStr
    
    
    
class UserCreate(UserBase):
    password: str = Field(...,min_length=8, max_length=100) 
    role: Literal["student","admin"] = "student"
    
    
class UserUpdate(BaseModel):
    name: str | None = Field(None,min_length=2, max_length=50)
    email: EmailStr | None = None
    is_active: bool | None = None
    
    
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    role: str
    is_active: bool
    created_at: datetime            