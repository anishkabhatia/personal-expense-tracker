from datetime import date, datetime
from pydantic import BaseModel, Field
from decimal import Decimal
# from typing import Literal

# CategoryType = Literal[app.constants.categories.CATEGORY_CHOICES]

class TransactionCreate(BaseModel):
    transaction_date: date
    merchant: str = Field(
        min_length=1, 
        max_length=255
    )
    amount: float = Field(gt=0)

    category: str = "Other"

    payment_source: str | None = None

    notes: str | None = None

class TransactionResponse(BaseModel):
    id: str

    transaction_date: date

    merchant: str

    amount: float

    category: str

    payment_source: str | None

    notes: str | None

    created_at: datetime | None = None

    is_split: bool = False

class TransactionUpdate(BaseModel):
    category: str | None = None

    notes: str | None = None