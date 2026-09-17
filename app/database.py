#********************connection file***************


from sqlalchemy.ext.asyncio import async_sessionmaker , create_async_engine
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL=os.getenv("DATABASE_URL")
engine=create_async_engine(DB_URL,echo=True)
SessionLocal=async_sessionmaker(bind=engine)#whenever a new user wants db connection


class Base(DeclarativeBase):#sqlalcehmy class now upcoming all table classess will inherit from this
    pass




