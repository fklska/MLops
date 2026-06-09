from core.models import Reviews
from settings import settings
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import sessionmaker

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
# "postgresql://postgres:1234567@localhost:5432/app"
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

ID_2_LABEL = {
    0: "NEUTRAL",
    1: "POSTIVE",
    2: "NEGATIVE",
}
LABEL_2_ID = {"NEUTRAL": 0, "POSTIVE": 1, "NEGATIVE": 2}


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


def get_training_data():
    with SessionLocal() as session:
        reviews = session.execute(
            select(Reviews.description, Reviews.label, Reviews.id).where(
                Reviews.trained.is_(False), Reviews.label.isnot(None)
            )
        ).fetchall()

    texts = [row[0] for row in reviews]
    labels = [LABEL_2_ID[row[1]] for row in reviews]
    ids = [row[2] for row in reviews]
    return texts, labels, ids


def mark_reviews_as_trained(review_ids: list[int]):
    with SessionLocal() as session:
        session.execute(update(Reviews).where(Reviews.id.in_(review_ids)).values(trained=True))
        session.commit()
