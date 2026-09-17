from fastapi import FastAPI
from contextlib import asynccontextmanager

# Import database engine and blueprint
from app.database import engine, Base
# Import all models so Base.metadata knows they exist before creating tables
from app.models import user, product 
# Import the modular routes
from app.routers import users

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server creating tables....")
    async with engine.begin() as connection:
       # Look at models.py and create any tables that don't exist yet in Postgres
       await connection.run_sync(Base.metadata.create_all)
    print("Tables created......")
    
    yield
    print("SERVER STOPPING: Cleaning up resources...")

# Initialize FastAPI
app = FastAPI(lifespan=lifespan)

# Mount the router (equivalent to app.use('/users', userRoutes))
app.include_router(users.router)