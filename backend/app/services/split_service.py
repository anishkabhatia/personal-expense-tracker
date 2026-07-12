"""
Split Service

Responsible for managin shared expenses. 

A split expense consists of:
1. A parent transaction
2. One or more participant allocations. 

Example:
Nike Transaction - 28000
    - Me - 10000
    - Friend A - 9000
    - Friend B - 9000
    
The service validates split data, creates participant records, and updates teh transaction's split status. 
"""

from app.core.supabase import supabase
from fastapi import HTTPException

class SplitService:
    """
    Contains business logic related to split expenses.
    """
    @staticmethod
    def create_split(
        transaction_id: str,
        participants: list[dict]
    ):
        """
        Create participant allocations for a transaction. 
        
        Business Rules:
        1. The transaction must exist. 
        2. There must be exactly one participant marked as "me".
        3. The sum of participant amounts must equal the transaction amount.
        4. The transaction's split status is updated to True after successful participant creation.

        Args:
            transaction_id (str): The ID of the Parent transaction to split.
            participants (list[dict]): A list of participants containing their allocations.

        Returns:
            list[dict]: A list of newly created participant records.
        """

        # Fetch the transaction being split.
        transaction = (
            supabase
            .table("transactions")
            .select("*")
            .eq("id", transaction_id)
            .single()
            .execute()
        )

        # Prevent splits from being created for non-existent transactions.
        if not transaction.data:
            raise HTTPException(
                status_code=404,
                detail=f"Transaction with id {transaction_id} not found"
            )
        
        transaction_amount = float(transaction.data["amount"])

        # Ensure exactly one participant is marked as "me".
        me_count = sum(
            1
            for participant in participants
            if participant["is_me"]
        )

        if me_count != 1:
            raise HTTPException(
                status_code=400,
                detail="There must be exactly one participant marked as 'me'"
            )
        
        # Validate that the sum of participant amounts equals the transaction amount.
        participant_total = sum(
            participant["amount"]
            for participant in participants
        )

        if round(participant_total, 2) != round(transaction_amount, 2):
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Participant total "
                    f"({participant_total}) "
                    f"does not equal transaction amount "
                    f"({transaction_amount})"
                )
            )
        
        # Convert participant data into rows for insertion into the database.
        rows = []
        
        for participant in participants:
            rows.append(
                {
                    "transaction_id": transaction_id,
                    "participant_name": participant["participant_name"],
                    "amount": participant["amount"],
                    "is_me": participant["is_me"]
                }
            )
        
        # Create participant records in the database.
        response = (
            supabase
            .table("split_participants")
            .insert(rows)
            .execute()
        )

        # Mark the parent transaction as a split transaction after successful participant creation.
        supabase.table("transactions").update(
            {
                "is_split": True
            }
        ).eq("id", transaction_id).execute()

        return response.data