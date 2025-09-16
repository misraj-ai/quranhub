from sqlalchemy.ext.asyncio import create_async_engine
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

# Load environment variables from .env file
load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
ASYNC_SQLALCHEMY_DATABASE_URL=SQLALCHEMY_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")


# Create an async engine with optimized connection pooling
async_engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URL,
    echo=False,  # Set to True only for debugging
    pool_size=10,  
    max_overflow=20,  
    pool_recycle=1800  
)

# Create an async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False
)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True