from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):#upcoming json request
    username:str
    email:str
class Update(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
