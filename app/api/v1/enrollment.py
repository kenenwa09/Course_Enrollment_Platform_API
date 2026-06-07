from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db, get_current_user, require_role
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse, EnrollmentDetail
from app.services.enrollment import EnrollmentService
from app.models.users import User


router = APIRouter(prefix="/enrollment", tags=["Enrollment"])



@router.get("/me", response_model=list[EnrollmentResponse], status_code=status.HTTP_200_OK)
async def my_enrollments(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await EnrollmentService.get_my_enrollments(db, current_user, skip=skip, limit=limit)




@router.get("/course/{course_id}", response_model= list[EnrollmentDetail], status_code=status.HTTP_200_OK)
async def list_course_enrollments(course_id: int, skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db), _: User = Depends(require_role)):
    return await EnrollmentService.get_course_enrollments(db, course_id, skip=skip, limit=limit)





@router.get("/", response_model= list[EnrollmentResponse], status_code=status.HTTP_200_OK)
async def list_all_enrollments(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db), _: User = Depends(require_role)):
    return await EnrollmentService.get_all_enrollments(db, skip=skip, limit=limit)



@router.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def enroll(data: EnrollmentCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await EnrollmentService.enroll(db, data, current_user)




@router.delete("/admin/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_remove_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(require_role)):
    await EnrollmentService.admin_remove_enrollment(db, enrollment_id)

    



@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unenroll(enrollment_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    await EnrollmentService.unenroll(db, enrollment_id, current_user)
    
