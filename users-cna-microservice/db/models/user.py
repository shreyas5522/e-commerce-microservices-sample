
# db/models/user.py
from typing import Optional
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from db.config import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Use String to preserve leading zeros and country codes (e.g., +91...)
    name:   Mapped[str]  = mapped_column(String(120), nullable=False)
    email:  Mapped[str]  = mapped_column(String(255), nullable=False, unique=True, index=True)
    mobile: Mapped[str]  = mapped_column(String(20),  nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r}, name={self.name!r}, mobile={self.mobile!r})"
