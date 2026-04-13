from app.core.db import Base
from sqlalchemy import BigInteger, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Films(Base):
    __tablename__ = "film"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    title: Mapped[str]
    year: Mapped[int]
    description: Mapped[str]
    reviews: Mapped[list["Reviews"]] = relationship(back_populates="film", cascade="all, delete-orphan")


class Reviews(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    film_id: Mapped[int] = mapped_column(ForeignKey("film.id"))
    film: Mapped["Films"] = relationship(back_populates="reviews")
