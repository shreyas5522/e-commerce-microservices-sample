
# db/models/schemas.py  (no changes needed)
from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr
    mobile: str  # store as string

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
