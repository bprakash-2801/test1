"""
Sample tests for the API
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from app.database import Base, get_db

# Test database URL (use SQLite for testing)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Setup test database before each test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Fraud Detection System API"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_user():
    """Test user creation"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "password123"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_get_users():
    """Test getting all users"""
    # First create a user
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "password123"
    }
    client.post("/api/v1/users/", json=user_data)
    
    # Then get all users
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_create_transaction():
    """Test transaction creation"""
    # First create a user
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "password123"
    }
    user_response = client.post("/api/v1/users/", json=user_data)
    user_id = user_response.json()["id"]
    
    # Create transaction
    transaction_data = {
        "transaction_id": "TXN001",
        "user_id": user_id,
        "amount": 100.50,
        "currency": "USD",
        "merchant": "Test Merchant",
        "category": "Shopping"
    }
    response = client.post("/api/v1/transactions/", json=transaction_data)
    assert response.status_code == 201
    data = response.json()
    assert data["transaction_id"] == "TXN001"
    assert data["amount"] == 100.50
