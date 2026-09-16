from database import Base,get_db,engine
from models import User
from schemas import UserCreate,Update
from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("server creating tables....")
    async with engine.begin() as connection:#open a connection to manage tbales
        # This tells SQLAlchemy: "Look at models.py and create any tables that don't exist yet in Postgres"
       await connection.run_sync(Base.metadata.create_all)
    print("Tables created......")
    # The yield keyword PAUSES this function while the server runs.
    # It just sits here waiting while people use your API.
    yield
    
    # If you press Ctrl+C to stop the server, the code resumes here.
    print("SERVER STOPPING: Cleaning up resources...")

app=FastAPI(lifespan=lifespan)
@app.post("/users")
async def create_user(user_data:UserCreate,db:AsyncSession=Depends(get_db)):
    new_user=User(
        username=user_data.username,
        email=user_data.email
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message":"Successfully created","new_user":new_user}

@app.get("/users")
async def get_users(db:AsyncSession=Depends(get_db)):
    query=select(User)
    result=await db.execute(query)
    users=result.scalars().all()
    return {"users":users}

# Why .scalars().all()?
# When db.execute(query) runs, it returns a raw database "chunk" that looks like a complex grid (like an Excel spreadsheet).

# .scalars() takes that grid and extracts just the first column (which contains your full User objects).

# .all() converts them into a standard Python list.



@app.get("/users/{user_id}")
async def get_by_id(user_id:int,db:AsyncSession=Depends(get_db)):
    query=select(User).where(User.id==user_id)
    result=await db.execute(query)
    user=result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404,message="User not found")
    return {"users":user}


@app.put("/users/{user_id}")
async def update_user(user_id:int,user_data:Update,db:AsyncSession=Depends(get_db)):
    query=select(User).where(user_id==User.id)
    result=await db.execute(query)
    user=result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    
    if user_data.username is not None:
        user.username=user_data.username
    if user_data.email is not None:
        user.email=user_data.email

    await db.commit()
    await db.refresh(user)

    return {"message": "User updated", "user": user}



@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    
    # 1. Fetch the user
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    # 2. Tell the session to delete this object
    await db.delete(user)
    
    # 3. Commit the transaction to finalize the deletion
    await db.commit()
    
    return {"message": f"User {user_id} has been deleted successfully"}