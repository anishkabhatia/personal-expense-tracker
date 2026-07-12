from app.core.supabase import supabase
from app.schemas.dashboard import DashboardSummary
from app.constants.categories import INVESTMENT_CATEGORY
from datetime import date
from calendar import monthrange


class DashboardService:

    @staticmethod
    def get_summary():
        today = date.today()

        start_of_month = date(
            today.year,
            today.month,
            1
        )

        end_of_month = date(
            today.year,
            today.month,
            monthrange(today.year, today.month)[1]
        )

        transactions_response = (
            supabase
            .table("transactions")
            .select("*")
            .gte("transaction_date", start_of_month.isoformat())
            .lte("transaction_date", end_of_month.isoformat())
            .execute()
        )

        transactions = transactions_response.data

        monthly_transactions_ids = {
            transaction["id"]
            for transaction in transactions
        }

        split_response = (
            supabase
            .table("split_participants")
            .select("*")
            .execute()
        )

        split_participants = split_response.data

        split_transaction_count = sum(
            1
            for transaction in transactions
            if transaction.get("is_split")
        )

        personal_spend = 0.0
        investments = 0.0
        money_owed_to_me = 0.0

        for transaction in transactions:
            category = transaction["category"]

            amount = float(transaction["amount"])

            is_split = transaction.get("is_split", False)

            if category == INVESTMENT_CATEGORY:
                investments += amount
                continue

            if not is_split:
                personal_spend += amount

        for participant in split_participants:
            amount = float(participant["amount"])
            transaction_id = participant["transaction_id"]

            #Personla Spend (Monthly)
            if ( transaction_id in monthly_transactions_ids and participant["is_me"] ):
                personal_spend += amount

            #Money Owed to Me (All Time)
            if (
                not participant["is_me"]
                and not participant["reimbursement_received"]
                ):
                money_owed_to_me += amount

        return DashboardSummary(
            personal_spend_this_month=round(personal_spend, 2),
            investments_this_month=round(investments, 2),
            money_owed_to_me=round(money_owed_to_me, 2),
            transaction_count=len(transactions),
            split_transaction_count=split_transaction_count
        )