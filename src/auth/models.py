# database models

from sqlalchemy import Column, Integer, String, Boolean, Enum
from enum import Enum as PyEnum
from src.models import Base
from sqlalchemy.orm import Mapped, mapped_column

class Role(PyEnum):
    ADMIN = 1
    STAFF = 2
    USER = 3
    GUEST = 4

class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(index=True, unique=True)
    slug: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    hashed_password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.GUEST)
