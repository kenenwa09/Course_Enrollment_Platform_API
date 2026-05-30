from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class CourseBase(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    code: str = Field(min_length=3, max_length=20)
    capacity: int = Field(...,gt=0)
    
    
class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: str | None = Field(None, min_length=5, max_length=100)
    code: str | None = Field(None, min_length=3, max_length=20)
    capacity: int | None = Field(None, gt=0)
    is_active: bool | None = None


class CourseResponse(CourseBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    created_at: datetime