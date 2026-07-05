from app.core.supabase import supabase
from app.schemas.transaction import TransactionCreate


class TransactionService:

    @staticmethod
    def get_all_transactions():
        response = (
            supabase
            .table("transactions")
            .select("*")
            .order("transaction_date", desc=True)
            .execute()
        )

        return response.data
    
    @staticmethod
    def create_transaction(transaction: TransactionCreate):
        response = (
            supabase
            .table("transactions")
            .insert(
                {
                    "transaction_date": transaction.transaction_date.isoformat(),
                    "merchant": transaction.merchant,
                    "amount": transaction.amount,
                    "category": transaction.category,
                    "payment_source": transaction.payment_source,
                    "notes": transaction.notes,
                    "is_split": False
                }
            )
            .execute()
        )

        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=500, detail="Failed to create transaction")

        return response.data[0]