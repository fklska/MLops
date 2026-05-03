from core.models import Reviews
from settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

ID_2_LABEL = {0: "NEGATIVE", 1: "POSTIVE"}
LABEL_2_ID = {"NEGATIVE": 0, "POSTIVE": 1}


def update_review_label(review_id: int, label: int, prob: float, status: str = "COMPLETED"):

    with SessionLocal() as session:
        db_review = session.get(Reviews, review_id)

        if db_review:
            db_review.label = label
            db_review.label_id = LABEL_2_ID[label]
            db_review.probability = prob
            db_review.status = status

            session.commit()
            session.refresh(db_review)
            return db_review

        return None
