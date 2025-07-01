from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

# Data being send from user to us
class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True
    
class CreatePost(PostBase):
    pass
    
class UpdatePost(PostBase):
    title : str
    content : str
    # published : bool
    
class UserOut(BaseModel):
    id : int
    email: EmailStr
    created_at : datetime
    
    class Config:
        from_attributes = True

# Data being send from us to user
class PostResponse(PostBase):
    id : int
    created_at : datetime
    user_id : int
    user : UserOut
    
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int
    
    # class Config:
        # from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str  

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token : str
    token_type : str
    
class TokenData(BaseModel):
    id : Optional[str] = None
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)   # type: ignore