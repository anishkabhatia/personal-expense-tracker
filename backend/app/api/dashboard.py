"""
Dashboard API Router

Defines dashboard related API endpoints. 

Responsibilities:
- Receive dashboard requests from the client
- Delegate business logic to DashboardService
- Return dashboard metrics to the caller

This router intentionally contains no calculation logic. 
All dashboard calculations belong in DashboardService. 
"""

from fastapi import APIRouter

from app.services.dashboard_service import (
    DashboardService
)

router = APIRouter()

@router.get("/summary")
def get_summary():
    """
    Retrieve dashboard summary metrics. 
    
    Returns:
    - Personal spend this month. 
    - Investments this month.
    - Money owed to me. 
    - Transaction count.
    - Split transaction count. 
    
    Flow:
        Client request -> Dashboard Service -> Supabase -> Dashboard Summary Response
    """
    return DashboardService.get_summary()