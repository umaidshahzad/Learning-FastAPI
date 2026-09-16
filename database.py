from sqlalchemy.ext.asyncio import async_sessionmaker , create_async_engine
from sqlalchemy.orm import DeclarativeBase

DB_URL="postgresql+asyncpg://admin:password123@localhost/practice_db"
engine=create_async_engine(DB_URL,echo=True)
SessionLocal=async_sessionmaker(bind=engine)#whenever a new user wants db connection


class Base(DeclarativeBase):#sqlalcehmy class now upcoming all table classess will inherit from this
    pass

async def get_db():
    db=SessionLocal()#open connection
    try:
        yield db#PAUSE: Hand the connection to the route. Wait until the route finishes sending a response
    finally:
        await db.close()


