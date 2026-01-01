
# db/dals/user_dal.py
from typing import List, Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.user import User

class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, name: str, email: str, mobile: str) -> User:
        """Create a new user and return the ORM instance."""
        new_user = User(name=name, email=email, mobile=mobile)
        self.db_session.add(new_user)
        # Flush so that new_user.id is populated on SQLite
        await self.db_session.flush()
        return new_user

    async def get_all_users(self) -> List[User]:
        """Return all users ordered by id."""
        res = await self.db_session.execute(select(User).order_by(User.id))
        return res.scalars().all()

    async def get_user(self, user_id: int) -> Optional[User]:
        """Return a single user by id, or None if not found."""
        res = await self.db_session.execute(select(User).where(User.id == user_id))
        return res.scalar()

    async def update_user(
        self,
        user_id: int,
        name: Optional[str],
        email: Optional[str],
        mobile: Optional[str],
    ) -> None:
        """Update fields for a user by id."""
        q = update(User).where(User.id == user_id)
        if name is not None:
            q = q.values(name=name)
        if email is not None:
            q = q.values(email=email)
        if mobile is not None:
            q = q.values(mobile=mobile)

        # Keep session synchronized
        q = q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)
