"""
Fraud Log model for tracking fraud detection events
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class FraudLog(Base):
    """Fraud Log model"""
    __tablename__ = "fraud_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    detection_method = Column(String(50))  # ml_model, rule_based, manual
    fraud_score = Column(Float, nullable=False)
    confidence = Column(Float)
    reason = Column(Text)
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    transaction = relationship("Transaction", backref="fraud_logs")
    
    def __repr__(self):
        return f"<FraudLog(id={self.id}, transaction_id={self.transaction_id}, fraud_score={self.fraud_score})>"
