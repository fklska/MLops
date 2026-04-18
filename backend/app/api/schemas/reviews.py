from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class ReviewBase(BaseModel):
    title: str
    description: str
    film_id: int


class ReviewRequest(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    film_id: Optional[int] = None


class Review(ReviewBase):
    id: int
    status: str
    label: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class ReviewResponse(BaseModel):
    reviews: List[Review]
    details: Optional[str] = None
