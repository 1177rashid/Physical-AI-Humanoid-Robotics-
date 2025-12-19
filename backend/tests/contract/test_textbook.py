import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.models import Base
from src.config.database import SessionLocal


# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_textbook.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    """Create a test client for the API"""
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[SessionLocal] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


def test_get_textbook_modules_contract(client):
    """Contract test for /textbook/modules endpoint"""
    response = client.get("/v1/textbook/modules")

    # Check that the response has the expected status code
    assert response.status_code == 200

    # Check that the response has the expected structure
    assert "data" in response.json()
    assert "total" in response.json()

    # Check that the data is a list
    assert isinstance(response.json()["data"], list)

    # Check that total is an integer
    assert isinstance(response.json()["total"], int)


def test_get_textbook_module_by_id_contract(client):
    """Contract test for /textbook/modules/{id} endpoint"""
    # Test with a sample UUID (this will likely return 404 since the module doesn't exist)
    sample_id = "123e4567-e89b-12d3-a456-426614174000"
    response = client.get(f"/v1/textbook/modules/{sample_id}")

    # Check that the response has an expected status code (either 200 or 404)
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        # If module exists, check the response structure
        response_data = response.json()
        assert "id" in response_data
        assert "title" in response_data
        assert "content" in response_data
        assert "category" in response_data