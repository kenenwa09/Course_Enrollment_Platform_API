from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db, require_role
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.services.course import CourseService
from app.models.users import User


router = APIRouter(prefix="/course", tags=["Course"])


@router.get("/", response_model=list[CourseResponse], status_code=status.HTTP_200_OK)
async def list_courses(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
    return await CourseService.get_all(db, skip=skip, limit=limit, active_only=True)



@router.get("/{course_id}", response_model= CourseResponse, status_code=status.HTTP_200_OK)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    return await CourseService.get_by_id(db, course_id)



@router.post("/", response_model= CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(data: CourseCreate, db: AsyncSession = Depends(get_db), _: User = Depends(require_role)):
    return await CourseService.create(db, data)



@router.patch("/{course_id}", response_model= CourseResponse, status_code=status.HTTP_200_OK)
async def update_course(course_id: int, data: CourseUpdate, db: AsyncSession = Depends(get_db), _: User = Depends(require_role)):
    return await CourseService.update(db, course_id, data)




@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(require_role)):
    await CourseService.delete(db, course_id)