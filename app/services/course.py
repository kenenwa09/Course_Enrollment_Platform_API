from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.course import CourseRepository
from app.schemas.course import CourseCreate, CourseUpdate
from app.models.course import Course

class CourseService:
    
    @staticmethod
    async def get_course(self, db: AsyncSession, course_id: int) -> Course:
        course = await CourseRepository.get_by_id(db, course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with id {course_id} not found"
            )
        return course
    
    
    
    @staticmethod
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 20, active_only: bool = True) -> list[Course]:
        return await CourseRepository.get_all(db, skip=skip, limit=limit, active_only=active_only)
    
    
    
    @staticmethod
    async def get_by_id(self, db: AsyncSession, course_id: int) -> Course:
        return await self.get_course(db, course_id)
    
    
    
    @staticmethod
    async def create(self, db: AsyncSession, data: CourseCreate) -> Course:
        existing = await CourseRepository.get_by_code(db, data.code)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Course code '{data.code}' is already taken"
            )   
            
        return await CourseRepository.create(db, data)
    
    
    
    
    @staticmethod
    async def update(self, db: AsyncSession, course_id: int, data: CourseUpdate) -> Course:
        course = await self.get_course(db, course_id)
        
        if data.code and data.code != course.code:
            existing = await CourseRepository.get_by_code(db, data.code)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Course code '{data.code}' is already taken"
                ) 
                
        return await CourseRepository.update(db, course, data)
    
    
    
    
    @staticmethod
    async def delete(self, db: AsyncSession, course_id: int) -> None:
        course = await self.get_course(db, course_id)
        await CourseRepository.delete(db, course)        