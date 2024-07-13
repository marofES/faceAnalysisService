from sqlalchemy import Boolean, Column, Enum, String
from sqlalchemy.ext.declarative import declarative_base
from src.auth.constants import RoleEnum

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
