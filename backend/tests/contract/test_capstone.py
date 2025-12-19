import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.models import Base
from src.config.database import SessionLocal


# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_capstone.db"

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


def test_get_capstone_projects_contract(client):
    """Contract test for /capstone/projects endpoint"""
    response = client.get("/v1/capstone/projects")

    # Check that the response has the expected status code
    assert response.status_code == 200

    # Check that the response has the expected structure
    response_data = response.json()
    assert "data" in response_data
    assert "total" in response_data

    # Check that the data is a list
    assert isinstance(response_data["data"], list)

    # Check that total is an integer
    assert isinstance(response_data["total"], int)


def test_get_capstone_project_by_id_contract(client):
    """Contract test for /capstone/projects/{id} endpoint"""
    # Test with a sample UUID (this will likely return 404 since the project doesn't exist)
    sample_id = "123e4567-e89b-12d3-a456-426614174000"
    response = client.get(f"/v1/capstone/projects/{sample_id}")

    # Check that the response has an expected status code (either 200 or 404)
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        # If project exists, check the response structure
        response_data = response.json()
        assert "id" in response_data
        assert "title" in response_data
        assert "description" in response_data
        assert "overview" in response_data


def test_voice_command_processing_contract(client):
    """Contract test for /chat endpoints related to voice commands"""
    # Prepare sample voice command data
    sample_command = {
        "sessionId": "123e4567-e89b-12d3-a456-426614174000",
        "voiceInput": "Move the robot forward by 1 meter",
        "context": "capstone-project"
    }

    response = client.post("/v1/chat/voice-command", json=sample_command)

    # Check that the response has an expected status code
    assert response.status_code in [200, 400, 401]

    if response.status_code == 200:
        # If successful, check the response structure
        response_data = response.json()
        assert "response" in response_data
        assert "action" in response_data