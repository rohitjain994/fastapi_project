from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Item(BaseModel):
    id: Optional[int] = Field(None, ge=1, description="Auto-incremented item identifier")
    name: str = Field(..., min_length=1, max_length=100, description="Name of the item")
    description: Optional[str] = Field(None, max_length=500, description="Optional item description")
    price: float = Field(..., ge=0, description="Item price (non-negative)")
    is_available: bool = Field(True, description="Availability flag")


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., ge=0)
    is_available: bool = Field(True)


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, ge=0)
    is_available: Optional[bool] = Field(None)


class UserCreate(BaseModel):
    email: EmailStr
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=6)


