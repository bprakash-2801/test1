"""
Pydantic schemas for FraudLog and Alert models
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FraudLogBase(BaseModel):
    """Base FraudLog schema"""
    detection_method: str = Field(..., max_length=50)
    fraud_score: float = Field(..., ge=0, le=1)
    confidence: Optional[float] = Field(None, ge=0, le=1)
    reason: Optional[str] = None


class FraudLogCreate(FraudLogBase):
    """Schema for creating a fraud log"""
    transaction_id: int


class FraudLogResponse(FraudLogBase):
    """Schema for fraud log response"""
    id: int
    transaction_id: int
    detected_at: datetime
    
    class Config:
        from_attributes = True


class AlertBase(BaseModel):
    """Base Alert schema"""
    alert_type: str = Field(..., max_length=50)
    severity: str = Field(..., max_length=20)
    message: str


class AlertCreate(AlertBase):
    """Schema for creating an alert"""
    transaction_id: int


class AlertUpdate(BaseModel):
    """Schema for updating an alert"""
    is_resolved: Optional[bool] = None
    resolved_by: Optional[int] = None


class AlertResponse(AlertBase):
    """Schema for alert response"""
    id: int
    transaction_id: int
    is_resolved: bool
    resolved_by: Optional[int] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
