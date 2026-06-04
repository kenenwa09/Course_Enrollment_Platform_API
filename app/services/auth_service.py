from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import UserRespository
from app. schemas.auth import LoginRequest, Token
from app.schemas.user import UserCreate, UserResponse
from app.core.security import verify_password, create_access_token
from app.models.users import User

class AuthService:
    
    @staticmethod
    async def register(db: AsyncSession, data: UserCreate) -> User:
        existing = await UserRespository.get_by_email(db, data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered"
            )
            
        user = await UserRespository.create(db,data)
        return user    
    
    
    
    @staticmethod
    async def login(db: AsyncSession, data: LoginRequest) -> Token:
        user = await UserRespository.get_by_email(db, data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
            
            
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )    
            
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )    
            
            
        access_token = create_access_token(data={"sub": user.email, "role": user.role})
        
        return Token(access_token=access_token, token_type="bearer")    