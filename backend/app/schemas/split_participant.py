from pydantic import BaseModel, Field


class SplitParticipantCreate(BaseModel):
    participant_name: str = Field(
        min_length=1,
        max_length=255
    )

    amount: float = Field(gt=0)

    is_me: bool = False


class SplitParticipantResponse(BaseModel):
    id: str

    transaction_id: str

    participant_name: str

    amount: float

    is_me: bool

    reimbursement_received: bool

class TransactionSplitCreate(BaseModel):
    participants: list[SplitParticipantCreate]