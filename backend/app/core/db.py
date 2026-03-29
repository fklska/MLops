from typing import Annotated

from app.core.config import settings
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session():
    async with async_session_maker() as session:
        yield session


Session = Annotated[AsyncSession, Depends(get_async_session)]


class Base(DeclarativeBase):
    pass
