from datetime import date, datetime
from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    transaction_date: date
    merchant: str = Field(
        min_length=1, 
        max_length=255
    )
    amount: float = Field(gt= 0)

    category: str = "Other"

    payment_source: str | None = None

    is_shared: bool = False

    personal_share: float | None = None

    notes: str | None = None

class TransactionResponse(BaseModel):
    id: str

    transaction_date: date

    merchant: str

    amount: float

    category: str

    payment_source: str | None

    is_shared: bool

    personal_share: float | None

    notes: str | None

    created_at: datetime | None = None

class TransactionUpdate(BaseModel):
    category: str | None = None

    is_shared: bool | None = None

    personal_share: float | None = None

    notes: str | None = None