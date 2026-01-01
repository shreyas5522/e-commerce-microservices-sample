
# routers/user_router.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from db.dals.user_dal import UserDAL
from db.models.schemas import UserOut
from dependencies import get_user_dal

router = APIRouter()

@router.post("/users", response_model=UserOut)
async def create_user(
    name: str,
    email: str,
    mobile: str,
    user_dal: UserDAL = Depends(get_user_dal),
):
    user = await user_dal.create_user(name, email, mobile)
    return user

@router.put("/users/{user_id}", response_model=None)
async def update_user(
    user_id: int,
    name: Optional[str] = None,
    email: Optional[str] = None,
    mobile: Optional[str] = None,
    user_dal: UserDAL = Depends(get_user_dal),
):
    await user_dal.update_user(user_id, name, email, mobile)
    return {"status": "ok"}

@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int,
    user_dal: UserDAL = Depends(get_user_dal),
):
    user = await user_dal.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users", response_model=List[UserOut])
async def get_all_users(
    user_dal: UserDAL = Depends(get_user_dal),
):
    return await user_dal.get_all_users()
