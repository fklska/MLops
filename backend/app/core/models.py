import enum
from typing import Optional

from app.core.db import Base
from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Films(Base):
    __tablename__ = "film"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), unique=True)
    year: Mapped[int]
    description: Mapped[str]
    reviews: Mapped[list["Reviews"]] = relationship(back_populates="film", cascade="all, delete-orphan")


class ReviewStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Reviews(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str] = mapped_column(Text)
    film_id: Mapped[int] = mapped_column(ForeignKey("film.id"))
    film: Mapped["Films"] = relationship(back_populates="reviews")
    status: Mapped[ReviewStatus] = mapped_column(
        Enum(ReviewStatus, name="review_status"),
        default=ReviewStatus.PENDING,
        server_default=ReviewStatus.PENDING.value,
        nullable=False,
    )

    label: Mapped[Optional[int]] = mapped_column(
        Integer, CheckConstraint("label IN (0, 1)", name="check_label_valid_values"), default=None, nullable=True
    )
