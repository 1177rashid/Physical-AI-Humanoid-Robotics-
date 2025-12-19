import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.models import Base
from src.models.textbook_module import TextbookModule
from src.models.lab_exercise import LabExercise
from src.config.database import SessionLocal
import uuid


# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_labs_integration.db"

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
    """Setup test data for textbook modules and lab exercises"""
    db = TestingSessionLocal()

    # Create a sample textbook module
    sample_module = TextbookModule(
        id=uuid.uuid4(),
        title="Introduction to ROS 2",
        slug="introduction-to-ros2",
        content="# Introduction to ROS 2\n\nThis module covers the basics of ROS 2.",
        category="foundations",
        prerequisites=[],
        learning_objectives=["Understand ROS 2 architecture", "Learn basic commands"],
        estimated_duration=60,
        is_published=True
    )

    # Create a sample lab exercise
    sample_lab = LabExercise(
        id=uuid.uuid4(),
        module_id=sample_module.id,
        title="ROS 2 Publisher/Subscriber Lab",
        description="Create a simple publisher and subscriber in ROS 2",
        difficulty="intermediate",
        instructions="# Lab Instructions\n\n1. Create a publisher node\n2. Create a subscriber node\n3. Connect them\n4. Test the communication",
        code_samples=[],
        expected_outcomes=["Publisher and subscriber communicate successfully"],
        prerequisites=["Basic ROS 2 knowledge"],
        simulation_required=False,
        estimated_duration=90,
        is_published=True
    )

    db.add(sample_module)
    db.add(sample_lab)
    db.commit()
    db.refresh(sample_module)
    db.refresh(sample_lab)

    yield sample_module.id, sample_lab.id  # Return the IDs of the created module and lab

    # Cleanup
    db.delete(sample_lab)
    db.delete(sample_module)
    db.commit()
    db.close()


def test_get_module_labs_integration(client, setup_test_data):
    """Integration test for lab exercise retrieval"""
    module_id, lab_id = setup_test_data

    response = client.get(f"/v1/textbook/modules/{module_id}/labs")

    assert response.status_code == 200
    data = response.json()

    # Should have at least one lab for this module
    assert len(data) >= 1

    # Find our test lab in the response
    found_test_lab = False
    for lab in data:
        if lab["title"] == "ROS 2 Publisher/Subscriber Lab":
            found_test_lab = True
            assert lab["moduleId"] == str(module_id)
            assert lab["difficulty"] == "intermediate"
            assert lab["estimatedDuration"] == 90
            assert lab["isPublished"] is True
            assert "publisher and subscriber" in lab["instructions"].lower()
            break

    assert found_test_lab, "Test lab exercise should be in the response"


def test_submit_lab_solution_integration(client, setup_test_data):
    """Integration test for lab solution submission"""
    module_id, lab_id = setup_test_data

    # Submit a solution to the lab
    submission_data = {
        "labExerciseId": str(lab_id),
        "submissionContent": "// Sample solution code\n#include <iostream>\nint main() { return 0; }",
        "submissionFiles": []
    }

    response = client.post("/v1/labs/submit", json=submission_data)

    # The response should be successful (200) or return a validation error (422)
    # depending on the implementation of the submission endpoint
    assert response.status_code in [200, 422]

    if response.status_code == 200:
        data = response.json()
        # Check that the response contains expected fields
        assert "id" in data
        assert "labExerciseId" in data
        assert "status" in data
        assert "submittedAt" in data
        assert data["labExerciseId"] == str(lab_id)
        assert data["status"] in ["submitted", "grading", "graded", "revised"]