from app.core.db_async import Base
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped,mapped_column, relationship
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.enrollment import Enrollment

class User(Base):
    __tablename__= "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[str] = mapped_column(String(20),nullable=False, default="student")
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    enrollments: Mapped[list["Enrollment"]] = relationship("Enrollment", back_populates="user", cascade="all, delete-orphan", lazy="selectin")


