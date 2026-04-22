from core.models import Reviews
from settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def update_review_label(review_id: int, label: int, status: str = "COMPLETED"):

    with SessionLocal() as session:
        db_review = session.get(Reviews, review_id)

        if db_review:
            db_review.label = label
            db_review.status = status

            session.commit()
            session.refresh(db_review)
            return db_review

        return None
