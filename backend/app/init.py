import os
from .database import engine, Base
from .models import PDF, Annotation, Note


def init_app():
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_app()
    print("Application initialized successfully!")
