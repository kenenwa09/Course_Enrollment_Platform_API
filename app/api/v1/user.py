from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, get_current_user, require_role
from app.schemas.user import UserResponse, UserUpdate
from app.services.user import UserService
from app.models.users import User


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user



@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def list_users(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db), _: User = Depends(require_role)):
    return await UserService.get_all(db, skip=skip, limit=limit)



@router.get("/{user_id}", response_model= UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(require_role)):
    return await UserService.get_user(db, user_id)



@router.patch("/{user_id}", response_model= UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, data: UserUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await UserService.update(db, user_id, data, current_user)



@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(require_role)):
    await UserService.delete(db, user_id)