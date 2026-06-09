from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class ReviewBase(BaseModel):
    title: str
    description: str


class ReviewRequest(ReviewBase):
    film_name: str


class ReviewUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class Review(ReviewBase):
    id: int
    film_id: int
    status: str
    label_id: Optional[int] = None
    label: Optional[str] = None
    probability: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class ReviewResponse(BaseModel):
    reviews: List[Review]
    details: Optional[str] = None
