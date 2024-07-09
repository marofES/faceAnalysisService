# database models

from sqlalchemy import Column, Integer, String, Boolean, Enum
from enum import Enum as PyEnum
from src.models import Base


class Role(PyEnum):
    admin = "admin"
    staff = "staff"
    n_user = "n_user"
    guest = "guest"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(Enum(Role), default=Role.n_user)