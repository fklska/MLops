from core.models import Reviews
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:1234567@localhost:5433/app")
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
