from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentCreate


class EnrollmentRepository:
    
    @staticmethod
    async def get_by_id(db: AsyncSession, enrollment_id: int) -> Enrollment | None:
        stmt = select(Enrollment).where(Enrollment.id == enrollment_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    
    @staticmethod
    async def get_by_id_with_details(db: AsyncSession, enrollment_id: int) -> Enrollment | None:
        stmt = select(Enrollment).where(Enrollment.id == enrollment_id).options(selectinload(Enrollment.user)).options(selectinload(Enrollment.course))
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    
    
    @staticmethod
    async def get_user_enrollments(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 20) -> list[Enrollment]:
        stmt = select(Enrollment).where(Enrollment.user_id == user_id).options(selectinload(Enrollment.course)).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().all())
    
    
    
    @staticmethod
    async def get_course_enrollments(db: AsyncSession, course_id: int, skip: int = 0, limit: int = 20) -> list[Enrollment] | None:
        stmt = select(Enrollment).where(Enrollment.course_id == course_id).options(selectinload(Enrollment.user)).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().all())
    
    
    
    @staticmethod
    async def get_all_enrollments(db: AsyncSession, skip: int = 0, limit: int = 20,) -> list[Enrollment]:
        stmt = (
            select(Enrollment)
            .options(selectinload(Enrollment.user))
            .options(selectinload(Enrollment.course))
            .offset(skip)
            .limit(limit)
        )
        
        result = await db.execute(stmt)
        return list(result.scalars().all())
    
    
    
    @staticmethod
    async def get_existing(self, db: AsyncSession, user_id: int, course_id: int) -> Enrollment | None:
        stmt = select(Enrollment).where(Enrollment.user_id == user_id, Enrollment.course_id == course_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
        
    
    
    @staticmethod
    async def create(db: AsyncSession, user_id: int, data: EnrollmentCreate) -> Enrollment:
        enrollment = Enrollment(
            user_id=user_id,
            course_id=data.course_id
        )
        db.add(enrollment)
        await db.commit()
        await db.refresh(enrollment)
        return enrollment
    
    
    @staticmethod
    async def delete(db: AsyncSession, enrollment: Enrollment) -> None:
        await db.delete(enrollment)
        await db.commit()