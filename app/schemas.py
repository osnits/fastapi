from pydantic import BaseModel, EmailStr, conint
from datetime import datetime 
from typing import Optional, List

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None


class PostCreate(PostBase):
    pass


class UserInfo(BaseModel):
    id: int 
    email: EmailStr
    #no pass for showing up
    created_at: datetime 
    
    class Config:
        #orm_mode = True
        orm_mode = True



class Post(PostBase): # response schema
    id: int
    created_at: datetime 
    owner_id: int
    owner: UserInfo

    class Config:
        # for convering Pyndantic model into SQLAlchemy
        #orm_mode = True
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str 


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel): # response schema
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    id: Optional[str] = None
 


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


class PostOut(BaseModel):
    Post: Post # the variable name must be capitalized 
    votes: int