# app/api/v1/routers.py
from fastapi import APIRouter
from .endpoints import health

router = APIRouter()
router.include_router(health.router, prefix="", tags=["health"])
