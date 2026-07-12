"""
Transaction Service

This service is resonsible for all transation related business logic. 

Responsibilities:
- Create new transactions
- Retrieve existing transactions
- Interact with the transactions table in Supabase

Why a service layer?
Teh API layer should not directly talk to the database. 

Instead:

API Endpoint -> Transaction Service -> Supabase Database

This keeps database logic centralized and makes the codebase easier to maintain, test and extend. 
"""

from fastapi import HTTPException
from app.core.supabase import supabase
from app.schemas.transaction import TransactionCreate


class TransactionService:
    """
    Contains Transaction related business logic. 
    
    All database interactions for transactions should live here rather than inside the API endpoint files.
    """
    @staticmethod
    def get_all_transactions():
        """
        Retrieve all transactions from the database. 
        
        Transactions are sorted by transaction date in descending order, so that the most recent transactions appear first.
        
        Returns:
            list[dict]: List of transactions records as dictionaries from Supabase.
            """
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
        """
        Create a new transactions. 
        
        Business Rules:
        1. Every new transaction starts as a non-split transaction.
        2. Split expenses are created later through the split workflow. 
        3. Input validation is handled by TransactionCrteate Pydantic schemas, so we can assume that the input data is valid.
        
        Args: 
            transaction: Validated transaction request payload.
        
        Returns:
            dict: Newly created transaction record. 
            
        Raises:
            HTTPException: If the transaction could not be created in the database.
        """
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

        # Defensive validation to ensure the insert succeeded and returned a valid record.
        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to create transaction")

        # Supabase returns inserted rows as a list. 
        # Since we are inserting a single transaction, we can safely return the first element of the list.
        return response.data[0]