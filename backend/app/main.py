from fastapi import FastAPI

from app.api.transactions import router as transactions_router
from app.api.dashboard import router as dashboard_router
app = FastAPI(
    title="Personal CFO API"
)

app.include_router(
    transactions_router,
    prefix="/transactions",
    tags=["transactions"]
)

app.include_router(
    dashboard_router,
    prefix="/dashboard",
    tags=["dashboard"]
)

@app.get("/")
def root():
    return {"status": "healthy"}