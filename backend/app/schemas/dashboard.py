from pydantic import BaseModel, ConfigDict


class DashboardSummary(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    personal_spend_this_month: float

    investments_this_month: float

    money_owed_to_me: float

    transaction_count: int

    split_transaction_count: int