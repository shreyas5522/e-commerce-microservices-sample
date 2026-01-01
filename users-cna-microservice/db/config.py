
# db/config.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

# Naming convention helps keep constraint names stable
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)

# Use SQLite async driver; adjust for Postgres/MySQL if needed
DATABASE_URL = "sqlite+aiosqlite:///./users.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,      # set True to log SQL
    future=True,
)

# Async session factory
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Alias to match your other imports (e.g., dependencies.py)
async_session = SessionLocal

# Dependency for FastAPI if you need it directly
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

# Optional initializer if you want to call it elsewhere
async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
