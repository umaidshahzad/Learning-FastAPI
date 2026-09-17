#*************Contains the User table******************
from sqlalchemy.orm import mapped_column,Mapped
from sqlalchemy import String, Boolean, Integer
from app.database import Base
class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email:Mapped[str]=mapped_column(String(50),unique=True)