"""
Transaction API Router

Defines all transaction related API endpoints. 

Responsibilities:
- Receive HTTP requests
- Validate request payloads using schemas
- Delegate business logic to services
- Return response to the client

The router should not contain database queries or business logic.
Those responsibilities belong to the service layer. 
"""

from fastapi import APIRouter
from app.services.transaction_service import TransactionService
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.schemas.split_participant import TransactionSplitCreate
from app.services.split_service import SplitService

router = APIRouter()

@router.get("/")
def get_transactions():
    """
    Retrieve all transactions. 
    
    Flow:
        Client Request -> TransactionService -> Supabse -> Response. 
        """
    return TransactionService.get_all_transactions()

@router.post("/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate):
    """
    Creates a new transaction. 
    
    FastAPI automatically validates teh request body using TransactionCreate before this function runs. 
    
    The response is validated against TransactionResponse. 
    """
    return TransactionService.create_transaction(transaction)

@router.post("/{transaction_id}/split")
def create_split(transaction_id: str, split: TransactionSplitCreate):
    """
    Create a split expense for an existing transaction. 
    
    Path Parameter:
        transaction_id
    
    Request_Body:
        participant allocations
        
    Example:
        - Nike 28000
            - Me 10000
            - Friend A 9000
            - Friend B 9000
    """
    return SplitService.create_split(
        transaction_id, 
        [
            participant.model_dump() for participant in split.participants
        ]
    )