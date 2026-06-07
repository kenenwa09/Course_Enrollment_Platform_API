from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.schemas.course import CourseCreate, CourseUpdate


class CourseRepository:
    
    @staticmethod
    async def get_by_id(db: AsyncSession, course_id: int) -> Course | None:
        stmt = select(Course).where(Course.id == course_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    
    @staticmethod
    async def get_by_code(db: AsyncSession, code: str) -> Course | None:
        stmt = select(Course).where(Course.code == code)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 20, active_only: bool = False) -> list[Course]:
        stmt = select(Course)
        if active_only:
            stmt = stmt.where(Course.is_active == True)
        stmt = stmt.offset(skip).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().all())
    
    
    @staticmethod
    async def create(db: AsyncSession, data: CourseCreate) -> Course:
        course = Course(
            title=data.title,
            code=data.code,
            capacity=data.capacity,
            is_active=data.is_active
        )
        db.add(course)
        await db.commit()
        await db.refresh(course)
        return course
    
    
    
    @staticmethod
    async def update(db: AsyncSession, course: Course, data: CourseUpdate) -> Course:
        update_data = data.model_dump(exclude_unset=True)
        for key,value in update_data.items():
            setattr(course, key, value)
        await db.commit()
        await db.refresh(course)
        return course
    
    
    
    @staticmethod
    async def delete(db: AsyncSession, course: Course) -> None:
        await db.delete(course)
        await db.commit()   
        
        
    @staticmethod    
    async def get_enrollment_count(db: AsyncSession, course_id: int) -> int:
        from sqlalchemy import select, func
        stmt = select(func.count()).where(Enrollment.course_id == course_id)
        result = await db.execute(stmt)
        return result.scalar_one()     