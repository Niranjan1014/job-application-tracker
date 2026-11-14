import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models.application import Application
from app.models.user import User
from app.security import hash_password, get_current_user

TEST_ENGINE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=TEST_ENGINE)
    db = TestingSessionLocal()
    user = User(email="test@example.com", hashed_password=hash_password("StrongPass123"))
    other = User(email="other@example.com", hashed_password=hash_password("OtherPass123"))
    db.add_all([user, other])
    db.commit()
    db.refresh(user)
    db.refresh(other)

    def override_get_db():
        try:
            yield db
        finally:
            pass

    def override_current_user():
        return user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_current_user
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    db.close()
    Base.metadata.drop_all(bind=TEST_ENGINE)


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_list_application(client):
    created = client.post(
        "/applications/",
        json={"company": "Germin8", "role": "AI Automation Intern"},
    )
    assert created.status_code == 201
    assert created.json()["company"] == "Germin8"

    listed = client.get("/applications/")
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_update_application_status(client):
    created = client.post(
        "/applications/",
        json={"company": "Example", "role": "Python Developer"},
    )
    app_id = created.json()["id"]
    updated = client.patch(f"/applications/{app_id}", json={"status": "Interview"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "Interview"


def test_invalid_status_rejected(client):
    created = client.post(
        "/applications/",
        json={"company": "Example", "role": "Python Developer"},
    )
    response = client.patch(
        f"/applications/{created.json()['id']}", json={"status": "Unknown"}
    )
    assert response.status_code == 400


def test_user_cannot_access_another_users_application(client):
    # Create a record owned by the second user, while the client is
    # authenticated as the first user.
    db = TestingSessionLocal()
    other_user = db.query(User).filter_by(email="other@example.com").one()
    private_application = Application(
        user_id=other_user.id,
        company="Private Co",
        role="Engineer",
    )
    db.add(private_application)
    db.commit()
    db.refresh(private_application)
    app_id = private_application.id
    db.close()

    response = client.get(f"/applications/{app_id}")
    assert response.status_code == 404
