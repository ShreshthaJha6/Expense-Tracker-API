from datetime import date as Date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ----------------------------
# User Schemas
# ----------------------------

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


# ----------------------------
# Expense Schemas
# ----------------------------

class ExpenseCreate(BaseModel):
    title: str = Field(..., min_length=2)
    amount: float = Field(..., gt=0)
    category: str
    description: Optional[str] = None
    date: Date


class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    date: Optional[Date] = None


class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    description: Optional[str]
    date: Date
    owner_id: int

    class Config:
        from_attributes = True