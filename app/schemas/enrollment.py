from pydantic import BaseModel,ConfigDict
from datetime import datetime
from app.schemas.user import UserResponse
from app.schemas.course import CourseResponse
    
    
class EnrollmentCreate(BaseModel):
    course_id: int


class EnrollmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    course_id: int
    user_id: int
    created_at: datetime 
    
#Admin use only    
class EnrollmentDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

    user: UserResponse
    course: CourseResponse       