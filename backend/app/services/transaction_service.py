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
                    "is_shared": transaction.is_shared,
                    "personal_share": transaction.personal_share,
                    "notes": transaction.notes
                }
            )
            .execute()
        )

        return response.data[0]