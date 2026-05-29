from app.core.db_async import Base
from typing import TYPE_CHECKING
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

if TYPE_CHECKING:
    from app.models.users import User
    from app.models.course import Course


class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    user: Mapped["User"] = relationship("User", back_populates="enrollments", lazy="selectin")
    
    course: Mapped["Course"] = relationship("Course", back_populates="enrollments", lazy="selectin")