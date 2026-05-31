from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.users import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password

class UserRespository:
    
    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    
    
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 20) -> list[User]:
        stmt = select(User).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalar().all())
    
    
    @staticmethod
    async def create(db: AsyncSession, data: UserCreate) -> User:
        user = User(
            name=data.name,
            email=data.email,
            hash_password=hash_password(data.password),
            role=data.role
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    
    @staticmethod
    async def update(db: AsyncSession, user: User, data: UserUpdate) -> User:
        update_data = data.model_dump(exclude_unset=True)
        for key,value in update_data.items():
            setattr(user, key, value)
        
        await db.commit()
        await db.refresh(user) 
        return user 
    
    
    
    @staticmethod
    async def delete(db: AsyncSession, user: User) -> None:
        await db.delete(user)
        await db.commit()  