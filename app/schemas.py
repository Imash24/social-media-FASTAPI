from typing import Optional
from pydantic import BaseModel, EmailStr

from datetime import datetime
from pydantic.types import conint

class PostBase(BaseModel):
    title : str 
    content : str
    published: bool = True
    
    
class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    


class Post(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut
    
    class Config:
        from_attributes = True   #orm mode has been changed to from attributes

class PostOut(BaseModel):
    Post: Post
    votes: int     
    
    class Config:
        from_attributes = True
        
        
class UserCreate(BaseModel):
    email : EmailStr
    password: str
    
    
    
    

    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
    
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore
    
    
    
    

    