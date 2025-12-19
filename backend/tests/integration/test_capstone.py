import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.models import Base
from src.models.capstone_project import CapstoneProject
from src.config.database import SessionLocal
import uuid


# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_capstone_integration.db"

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


@pytest.fixture
def setup_test_data():
    """Setup test data for capstone projects"""
    db = TestingSessionLocal()

    # Create a sample capstone project
    sample_project = CapstoneProject(
        id=uuid.uuid4(),
        title="Voice-Controlled Humanoid Robot Capstone",
        description="Develop a humanoid robot that responds to voice commands",
        overview="# Voice-Controlled Humanoid Robot\n\nThis project integrates all concepts learned in the textbook to create a robot that can understand and execute voice commands.",
        requirements=[
            "Implement voice recognition system",
            "Create motion planning algorithms",
            "Integrate perception and control systems"
        ],
        voice_integration_required=True,
        simulation_components=["Gazebo", "ROS 2"],
        evaluation_criteria=[
            "Robot responds correctly to voice commands",
            "Navigation accuracy > 90%",
            "Task completion rate > 85%"
        ],
        estimated_duration=120,  # hours
        is_published=True
    )

    db.add(sample_project)
    db.commit()
    db.refresh(sample_project)

    yield sample_project.id  # Return the ID of the created project

    # Cleanup
    db.delete(sample_project)
    db.commit()
    db.close()


def test_get_capstone_projects_integration(client, setup_test_data):
    """Integration test for capstone project retrieval"""
    project_id = setup_test_data

    response = client.get("/v1/capstone/projects")

    assert response.status_code == 200
    data = response.json()

    # Should have at least one project
    assert data["total"] >= 1
    assert len(data["data"]) >= 1

    # Find our test project in the response
    found_test_project = False
    for project in data["data"]:
        if project["title"] == "Voice-Controlled Humanoid Robot Capstone":
            found_test_project = True
            assert project["voiceIntegrationRequired"] is True
            assert project["estimatedDuration"] == 120
            assert project["isPublished"] is True
            assert "voice commands" in project["description"].lower()
            break

    assert found_test_project, "Test capstone project should be in the response"


def test_get_specific_capstone_project_integration(client, setup_test_data):
    """Integration test for retrieving a specific capstone project"""
    project_id = setup_test_data

    response = client.get(f"/v1/capstone/projects/{project_id}")

    assert response.status_code == 200
    data = response.json()

    # Check that the returned project matches our test data
    assert data["id"] == str(project_id)
    assert data["title"] == "Voice-Controlled Humanoid Robot Capstone"
    assert data["voiceIntegrationRequired"] is True
    assert data["estimatedDuration"] == 120
    assert "voice-control" in data["overview"].lower()
    assert len(data["requirements"]) > 0
    assert len(data["evaluationCriteria"]) > 0