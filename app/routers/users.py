from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.models.product import Product
from app.schemas.user import UserCreate,Update
from app.dependencies import get_db


router=APIRouter(prefix="/users",tags=["Users"])

@router.post("/")
async def create_user(user_data:UserCreate,db:AsyncSession=Depends(get_db)):
    new_user=User(
        username=user_data.username,
        email=user_data.email
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message":"Successfully created","new_user":new_user}

@router.get("/")
async def get_users(db:AsyncSession=Depends(get_db)):
    query=select(User)
    result=await db.execute(query)
    users=result.scalars().all()
    return {"users":users}

# Why .scalars().all()?
# When db.execute(query) runs, it returns a raw database "chunk" that looks like a complex grid (like an Excel spreadsheet).

# .scalars() takes that grid and extracts just the first column (which contains your full User objects).

# .all() converts them into a standard Python list.



@router.get("/{user_id}")
async def get_by_id(user_id:int,db:AsyncSession=Depends(get_db)):
    query=select(User).where(User.id==user_id)
    result=await db.execute(query)
    user=result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    return {"users":user}


@router.put("/{user_id}")#this user_id must match with the parameter given to this function
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



@router.delete("/{user_id}")
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