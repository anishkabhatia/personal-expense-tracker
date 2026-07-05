from fastapi import APIRouter
from app.services.transaction_service import TransactionService
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.schemas.split_participant import TransactionSplitCreate
from app.services.split_service import SplitService

router = APIRouter()


@router.get("/")
def get_transactions():
    return TransactionService.get_all_transactions()

@router.post("/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate):
    return TransactionService.create_transaction(transaction)

@router.post("/{transaction_id}/split")
def create_transaction_split(transaction_id: str, split: TransactionSplitCreate):
    return SplitService.create_split(
        transaction_id, 
        [
            participant.model_dump() for participant in split.participants
        ]
    )