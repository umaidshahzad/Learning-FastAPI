from app.database import SessionLocal

async def get_db():
    db=SessionLocal()#open connection
    try:
        yield db#PAUSE: Hand the connection to the route. Wait until the route finishes sending a response
    finally:
        await db.close()