from sqlalchemy.orm import mapped_column,Mapped
from sqlalchemy import String, Boolean, Integer
from database import Base
class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email:Mapped[str]=mapped_column(String(50),unique=True)




#To create another table, you simply write another class in your models.py file that inherits from Base.
# Just add the new class right below it!
class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)
