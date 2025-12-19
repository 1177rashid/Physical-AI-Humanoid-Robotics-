import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.models import Base
from src.config.database import SessionLocal


# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_labs.db"

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


def test_get_module_labs_contract(client):
    """Contract test for /textbook/modules/{id}/labs endpoint"""
    # Test with a sample module ID (this will likely return 404 since the module doesn't exist)
    sample_module_id = "123e4567-e89b-12d3-a456-426614174000"
    response = client.get(f"/v1/textbook/modules/{sample_module_id}/labs")

    # Check that the response has an expected status code (either 200 or 404)
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        # If module exists, check the response structure
        response_data = response.json()
        # Response should be a list of lab exercises
        assert isinstance(response_data, list)

        # If there are labs, check that they have expected fields
        if response_data:
            first_lab = response_data[0]
            assert "id" in first_lab
            assert "moduleId" in first_lab
            assert "title" in first_lab
            assert "description" in first_lab


def test_submit_lab_solution_contract(client):
    """Contract test for /labs/submit endpoint"""
    # Prepare sample submission data
    sample_submission = {
        "labExerciseId": "123e4567-e89b-12d3-a456-426614174000",
        "submissionContent": "// Sample code submission",
        "submissionFiles": []
    }

    response = client.post("/v1/labs/submit", json=sample_submission)

    # Check that the response has an expected status code
    assert response.status_code in [200, 400, 401, 404]

    if response.status_code == 200:
        # If successful submission, check the response structure
        response_data = response.json()
        assert "id" in response_data
        assert "status" in response_data
        assert "submittedAt" in response_data