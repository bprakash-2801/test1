"""
Database initialization script
Run this script to create all database tables
"""
from app.database import Base, engine
from app.models import User, Transaction, FraudLog, Alert

def init_db():
    """Initialize database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
