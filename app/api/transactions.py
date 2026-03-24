"""
Transaction API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import Transaction, User
from app.schemas import TransactionCreate, TransactionResponse, TransactionUpdate, TransactionList

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """
    Create a new transaction
    """
    # Verify user exists
    user = db.query(User).filter(User.id == transaction.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if transaction_id already exists
    existing = db.query(Transaction).filter(
        Transaction.transaction_id == transaction.transaction_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction ID already exists"
        )
    
    # Create new transaction
    db_transaction = Transaction(**transaction.model_dump())
    
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    return db_transaction


@router.get("/", response_model=TransactionList)
def get_transactions(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    status: Optional[str] = None,
    is_fraudulent: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Get all transactions with filtering and pagination
    """
    query = db.query(Transaction)
    
    # Apply filters
    if user_id:
        query = query.filter(Transaction.user_id == user_id)
    if status:
        query = query.filter(Transaction.status == status)
    if is_fraudulent is not None:
        query = query.filter(Transaction.is_fraudulent == is_fraudulent)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    transactions = query.offset(skip).limit(limit).all()
    
    return {"total": total, "transactions": transactions}


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """
    Get a specific transaction by ID
    """
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transaction


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a transaction
    """
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # Update transaction fields
    update_data = transaction_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_transaction, field, value)
    
    db.commit()
    db.refresh(db_transaction)
    
    return db_transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """
    Delete a transaction
    """
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    db.delete(db_transaction)
    db.commit()
    
    return None
