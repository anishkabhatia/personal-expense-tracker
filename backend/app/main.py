from fastapi import FastAPI

from app.api.transactions import router as transactions_router

app = FastAPI(
    title="Personal CFO API"
)

app.include_router(
    transactions_router,
    prefix="/transactions",
    tags=["transactions"]
)


@app.get("/")
def root():
    return {"status": "healthy"}