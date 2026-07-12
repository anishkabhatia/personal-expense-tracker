from fastapi import APIRouter

from app.services.dashboard_service import (
    DashboardService
)

router = APIRouter()


@router.get("/summary")
def get_summary():
    return DashboardService.get_summary()