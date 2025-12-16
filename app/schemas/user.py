from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    nome: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    nome: Optional[str] = None