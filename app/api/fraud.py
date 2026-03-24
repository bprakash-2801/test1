"""
Fraud detection API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import FraudLog, Alert, Transaction
from app.schemas import FraudLogCreate, FraudLogResponse, AlertCreate, AlertResponse, AlertUpdate

router = APIRouter(prefix="/fraud", tags=["fraud"])


# Fraud Logs endpoints
@router.post("/logs", response_model=FraudLogResponse, status_code=status.HTTP_201_CREATED)
def create_fraud_log(fraud_log: FraudLogCreate, db: Session = Depends(get_db)):
    """
    Create a new fraud log
    """
    # Verify transaction exists
    transaction = db.query(Transaction).filter(Transaction.id == fraud_log.transaction_id).first()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    db_fraud_log = FraudLog(**fraud_log.model_dump())
    
    db.add(db_fraud_log)
    db.commit()
    db.refresh(db_fraud_log)
    
    return db_fraud_log


@router.get("/logs", response_model=List[FraudLogResponse])
def get_fraud_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all fraud logs with pagination
    """
    fraud_logs = db.query(FraudLog).offset(skip).limit(limit).all()
    return fraud_logs


@router.get("/logs/{log_id}", response_model=FraudLogResponse)
def get_fraud_log(log_id: int, db: Session = Depends(get_db)):
    """
    Get a specific fraud log by ID
    """
    fraud_log = db.query(FraudLog).filter(FraudLog.id == log_id).first()
    if not fraud_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fraud log not found"
        )
    return fraud_log


# Alerts endpoints
@router.post("/alerts", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    """
    Create a new alert
    """
    # Verify transaction exists
    transaction = db.query(Transaction).filter(Transaction.id == alert.transaction_id).first()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    db_alert = Alert(**alert.model_dump())
    
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    
    return db_alert


@router.get("/alerts", response_model=List[AlertResponse])
def get_alerts(
    skip: int = 0,
    limit: int = 100,
    is_resolved: bool = None,
    severity: str = None,
    db: Session = Depends(get_db)
):
    """
    Get all alerts with filtering and pagination
    """
    query = db.query(Alert)
    
    if is_resolved is not None:
        query = query.filter(Alert.is_resolved == is_resolved)
    if severity:
        query = query.filter(Alert.severity == severity)
    
    alerts = query.offset(skip).limit(limit).all()
    return alerts


@router.get("/alerts/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    """
    Get a specific alert by ID
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    return alert


@router.put("/alerts/{alert_id}", response_model=AlertResponse)
def update_alert(alert_id: int, alert_update: AlertUpdate, db: Session = Depends(get_db)):
    """
    Update an alert (e.g., mark as resolved)
    """
    db_alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    # Update alert fields
    update_data = alert_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_alert, field, value)
    
    db.commit()
    db.refresh(db_alert)
    
    return db_alert
