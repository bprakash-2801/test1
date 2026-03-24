"""
Transaction model for storing financial transactions
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Transaction(Base):
    """Transaction model"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(100), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    merchant = Column(String(100))
    category = Column(String(50))
    location = Column(String(100))
    description = Column(String(255))
    is_fraudulent = Column(Boolean, default=False)
    fraud_score = Column(Float, default=0.0)
    status = Column(String(20), default="pending")  # pending, approved, flagged, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    user = relationship("User", backref="transactions")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, transaction_id='{self.transaction_id}', amount={self.amount})>"
