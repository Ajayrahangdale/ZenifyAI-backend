from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str  # ✅ Include password

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True  # ✅ SQLAlchemy to Pydantic conversion
