import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.models import Base
from src.models.textbook_module import TextbookModule
from src.config.database import SessionLocal
import uuid


# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_textbook_integration.db"

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
    """Setup test data for textbook modules"""
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

    db.add(sample_module)
    db.commit()
    db.refresh(sample_module)

    yield sample_module.id  # Return the ID of the created module

    # Cleanup
    db.delete(sample_module)
    db.commit()
    db.close()


def test_get_textbook_modules_integration(client, setup_test_data):
    """Integration test for textbook module retrieval"""
    response = client.get("/v1/textbook/modules")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) >= 1  # Should have at least the test module

    # Check if our test module is in the response
    found_test_module = False
    for module in data["data"]:
        if module["title"] == "Introduction to ROS 2":
            found_test_module = True
            assert module["category"] == "foundations"
            assert module["estimatedDuration"] == 60
            assert module["isPublished"] is True
            break

    assert found_test_module, "Test textbook module should be in the response"


def test_get_specific_textbook_module_integration(client, setup_test_data):
    """Integration test for retrieving a specific textbook module"""
    module_id = setup_test_data
    response = client.get(f"/v1/textbook/modules/{module_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Introduction to ROS 2"
    assert data["category"] == "foundations"
    assert data["estimatedDuration"] == 60
    assert data["isPublished"] is True
    assert "# Introduction to ROS 2" in data["content"]