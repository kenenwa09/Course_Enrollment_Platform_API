from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db, get_current_user
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.models.users import User


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await AuthService.register(db, data)



@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await AuthService.login(db, data)



@router.get("/me", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def me(current_user: User = Depends(get_current_user)):
    return current_user