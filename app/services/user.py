from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import UserRespository
from app.schemas.user import UserUpdate
from app.models.users import User


class UserService:
    
    @staticmethod
    async def get_user(db: AsyncSession, user_id: int) -> User:
        user = await UserRespository.get_by_id(db, user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return user
    
    
    
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int =20) -> list[User]:
        return await UserRespository.get_all(db, skip=skip, limit=limit)
    
    
    
    
    @staticmethod
    async def update(db: AsyncSession, user_id: int, data: UserUpdate, current_user: User) -> User:    
        user = await UserService.get_user(db, user_id)
        
        if current_user.role != "admin" and current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own profile"
            )
            
        if data.email and data.email != user.email:
            existing = await UserRespository.get_by_email(db, data.email)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email is already taken"
                )    
                
        return await UserRespository.update(db, user, data)
    
    
    
    @staticmethod
    async def delete(db: AsyncSession, user_id: int) -> None:
        user = await UserService.get_user(db, user_id)
        await UserRespository.delete(db, user)        