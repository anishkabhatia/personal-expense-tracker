from fastapi import APIRouter
from app.services.transaction_service import TransactionService
from app.schemas.transaction import TransactionCreate, TransactionResponse

router = APIRouter()


@router.get("/")
def get_transactions():
    return TransactionService.get_all_transactions()

@router.post("/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate):
    return TransactionService.create_transaction(transaction)
