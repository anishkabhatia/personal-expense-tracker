"""
Dashboard Service

Responsible for calculating and aggregating dashboard level financial metrics. 

Unlike other services that primarily perform CRUD operations, DashboardService combines data from multiple sources and applies financial business rules to generate meaningful insights. 

Data Sources:
- transactions
- split_participants

Key Responsibilities:
- Calculate personal spend for the current month. 
- Track investments seperately from spending. 
- Calculate oustanding reimbursements owed to the user. 
- Count transactions and split transactions. 
- Produce a dashboard summary for the frontend. 

Architechture Flow:
- Dashboard API -> Dashboard Service -> Transactions + Split Participants -> Financial Calculations -> DashboardSummary Response. 
    
Business Philosophy:
The dashboard answers:
1. How much money did I personally spend this month?
2. How much did I invest this month?
3. How much money am I still waiting to receive?
4. How many transactions have I made?
5. How many of those transactions were shared expenses?

This service acts as the financial reporting layer of the application.
"""

from app.core.supabase import supabase
from app.schemas.dashboard import DashboardSummary
from app.constants.categories import INVESTMENT_CATEGORY
from datetime import date
from calendar import monthrange


class DashboardService:
    """
    Service responsible for calculating dashboard-level financial metrics
    
    The dashboard combines information from:
    1. Transactions
    2. Split participants
    
    and produces a summarized financial view for the user.
    """

    @staticmethod
    def get_summary():
        """
        Returns dashboard metrics such as:
        
        - Personal spend this month
        - Investments this month
        - Money owed to me (all time)
        - Total transaction count
        - Split transaction count
        
        Business Rules:
        1. Personal spend should only include the current month's transactions.
        2. Investments should be tracked separately from spend.
        3. Money owed to me should include all outstanding reimbursements, regardless of the transaction date.
        """

        # Determine the current month's date range
        #Example:
        # If today is 2026-07-15, then:
        # start_of_month = 2026-07-01
        # end_of_month = 2026-07-31

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

        # Fetch only transactions belonging to the current month.
        # Dashboard spend and investment metrics are month-based,
        # so older transactions are intentionally excluded. 
        transactions_response = (
            supabase
            .table("transactions")
            .select("*")
            .gte("transaction_date", start_of_month.isoformat())
            .lte("transaction_date", end_of_month.isoformat())
            .execute()
        )

        transactions = transactions_response.data

        # Fetch all split participant records. 
        # We intentionally do not apply a month filter here because
        # money owed to the user may originate from older transactions
        # that still have outstanding reimbursements. 

        split_response = (
            supabase
            .table("split_participants")
            .select("*")
            .execute()
        )

        split_participants = split_response.data

        # Running totals to build the dashboard summary.
        personal_spend = 0.0
        investments = 0.0
        money_owed_to_me = 0.0

        # Create a quick lookup set containing all transations
        # belonging to the current month. 
        # Used later to determine whether a split participant
        # belongs to the current month or not.
        monthly_transaction_ids = {
            transaction["id"]
            for transaction in transactions
        }

        # Count how many current-month transactions are marked as split.
        split_transaction_count = sum(
            1
            for transaction in transactions
            if transaction.get("is_split")
        )

        # Process current month's transactions. 
        # Investment transactions are tracked separately and
        # are not included in personal spend.
        #
        # For non-split transactions:
        # the entire amount belongs to the user. 
        #
        # For split transactions:
        # User's share is calculated later using split participant records.

        for transaction in transactions:
            category = transaction["category"]
            amount = float(transaction["amount"])
            is_split = transaction.get("is_split", False)

            if category == INVESTMENT_CATEGORY:
                investments += amount
                continue

            if not is_split:
                personal_spend += amount

        # Process split participants.
        #
        # Personal Spend: Include only participants marked as "me" and belonging to the current month.
        # Money Owed to Me: Include all unreimbursed participants regardless of transaction date.
        for participant in split_participants:
            amount = float(participant["amount"])
            is_current_month = ( participant["transaction_id"] in monthly_transaction_ids )

            #Personal Spend (Monthly)
            if is_current_month and participant["is_me"]:
                personal_spend += amount

            #Money Owed to Me (All Time)
            if (
                not participant["is_me"]
                and not participant["reimbursement_received"]
                ):
                money_owed_to_me += amount

        # Return the final dashboard metrics. 
        return DashboardSummary(
            personal_spend_this_month=round(personal_spend, 2),
            investments_this_month=round(investments, 2),
            money_owed_to_me=round(money_owed_to_me, 2),
            transaction_count=len(transactions),
            split_transaction_count=split_transaction_count
        )