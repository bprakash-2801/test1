"""
Pydantic schemas for Transaction model
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TransactionBase(BaseModel):
    """Base Transaction schema"""
    transaction_id: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    currency: str = Field(default="USD", max_length=10)
    merchant: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=255)


class TransactionCreate(TransactionBase):
    """Schema for creating a transaction"""
    user_id: int


class TransactionUpdate(BaseModel):
    """Schema for updating a transaction"""
    status: Optional[str] = Field(None, max_length=20)
    is_fraudulent: Optional[bool] = None
    fraud_score: Optional[float] = Field(None, ge=0, le=1)


class TransactionResponse(TransactionBase):
    """Schema for transaction response"""
    id: int
    user_id: int
    is_fraudulent: bool
    fraud_score: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class TransactionList(BaseModel):
    """Schema for list of transactions"""
    total: int
    transactions: list[TransactionResponse]
