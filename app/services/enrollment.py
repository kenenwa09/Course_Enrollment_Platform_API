from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.enrollment import EnrollmentRepository
from app.repositories.course import CourseRepository
from app.schemas.enrollment import EnrollmentCreate
from app.models.enrollment import Enrollment
from app.models.users import User


class EnrollmentService:
    
    @staticmethod
    async def enroll(db: AsyncSession, data: EnrollmentCreate, current_user: User) -> Enrollment:
        if current_user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can enroll in courses"
            )
            
        course = await CourseRepository.get_by_id(db, data.course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )    
            
            
        if not course.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot enroll in an inactive course"
            )    
            
            
        existing = await EnrollmentRepository.get_existing(db, current_user.id, data.course_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are already enrolled in this course"
            )    
            
            
            
        count = await CourseRepository.get_enrollment_count(db, data.course_id)
        if count >= course.capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Course has reached maximum capacity"
            )    
            
        return await EnrollmentRepository.create(db, current_user.id, data)
    
    
    
    
    @staticmethod
    async def unenroll(db: AsyncSession, enrollment_id: int, current_user: User) -> None:
        enrollment = await EnrollmentRepository.get_by_id(db, enrollment_id)
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found"
            )    
            
            
        if current_user.role == "student" and enrollment.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only deregister from your own enrollments"
            )     
            
        await EnrollmentRepository.delete(db, enrollment)
        
        
        
        
    @staticmethod
    async def get_my_enrollments(db: AsyncSession, current_user: User, skip: int = 0, limit: int = 20) -> list[Enrollment]:
        return await EnrollmentRepository.get_user_enrollments(db, current_user.id, skip=skip, limit=limit)
    
    
    
    @staticmethod
    async def get_all_enrollments(db: AsyncSession, skip: int = 0, limit: int = 20) -> list[Enrollment]:
        return await EnrollmentRepository.get_all_enrollments(db, skip=skip, limit=limit)
    
    
    
    
    @staticmethod
    async def get_course_enrollments(db: AsyncSession, course_id: int, skip: int = 0, limit: int = 20) -> list[Enrollment]:
        course = await CourseRepository.get_by_id(db, course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )        
            
        return await EnrollmentRepository.get_course_enrollments(db, course_id, skip=skip, limit=limit)
    
    
    
    
    @staticmethod
    async def admin_remove_enrollment(db: AsyncSession, enrollment_id: int) -> None:
        enrollment = await EnrollmentRepository.get_by_id(db, enrollment_id)
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found"
            )    
            
        await EnrollmentRepository.delete(db, enrollment)    