import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.models import Base, Task, Project, User
from app.config import settings

if "taskforge_test" not in settings.test_database_url:
    raise RuntimeError("Tests must use taskforge_test database")

test_engine = create_engine(settings.test_database_url)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def clean_database():
    yield

    with TestingSessionLocal() as db:
        db.execute(delete(Task))
        db.execute(delete(Project))
        db.execute(delete(User))
        db.commit()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client