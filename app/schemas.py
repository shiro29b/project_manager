# Pydantic models
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    name: str

class ProjectCreate(ProjectBase):
    project_manager_id: int
    client_id: int

class ProjectOut(ProjectBase):
    id: int
    project_manager: UserOut
    client: UserOut

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str]=None
