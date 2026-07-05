from app.core.supabase import supabase
from fastapi import HTTPException

class SplitService:

    @staticmethod
    def create_split(
        transaction_id: str,
        participants: list[dict]
    ):
        
        transaction = (
            supabase
            .table("transactions")
            .select("*")
            .eq("id", transaction_id)
            .single()
            .execute()
        )

        if not transaction.data:
            raise HTTPException(
                status_code=404,
                detail=f"Transaction with id {transaction_id} not found"
            )
        
        transaction_amount = float(transaction.data["amount"])

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
        
        response = (
            supabase
            .table("split_participants")
            .insert(rows)
            .execute()
        )

        supabase.table("transactions").update(
            {
                "is_split": True
            }
        ).eq("id", transaction_id).execute()
        
        return response.data