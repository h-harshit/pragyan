from models.base import Base
from models.mixins import TimeStampMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import UniqueConstraint, CheckConstraint


class Users(Base, TimeStampMixin):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="users_email_key"),
        CheckConstraint(
            "email ~* '^[\\w\\.-]+@[a-zA-Z\\d\\.-]+\\.[a-zA-Z]{2,}$'",
            name="email_pattern_check",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100))
    passhash: Mapped[str] = mapped_column(String(255), nullable=True)
