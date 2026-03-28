from db import Base
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Films(Base):
    __tablename__ = "film"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    title: Mapped[str]
    year: Mapped[int]
    description: Mapped[str]


class Reviews(Base):
    __tablename__ = "Review"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    film: Mapped[int] = relationship(back_populates="user", cascade="all, delete-orphan")
    title: Mapped[str]
    year: Mapped[int]
    description: Mapped[str]
