from typing import Literal
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()

class HealthResponse(BaseModel):
    status: Literal["ok"]

@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")
