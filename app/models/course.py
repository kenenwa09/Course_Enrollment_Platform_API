from app.core.db_async import Base
from datetime import datetime
from sqlalchemy import String, func
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.enrollment import Enrollment


class Course(Base):
    __tablename__ = "courses"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    code: Mapped[str] = mapped_column(String(20),unique=True, nullable=False)
    capacity: Mapped[int] = mapped_column(nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now()) 
    
    enrollments: Mapped[list["Enrollment"]] = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan", lazy= "selectin")