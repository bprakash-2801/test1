"""
API router initialization
"""
from fastapi import APIRouter
from app.api import users, transactions, fraud

api_router = APIRouter()

# Include all routers
api_router.include_router(users.router)
api_router.include_router(transactions.router)
api_router.include_router(fraud.router)
