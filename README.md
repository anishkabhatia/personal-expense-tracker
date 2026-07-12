# Personal Expense Tracker

Personal Expense Tracker is an AI-powered personal finance platform that helps users track their actual spending, especially when transactions involve shared expenses, reimbursements, and investments. Unlike traditional expense trackers, it distinguishes between money spent personally and money temporarily paid on behalf of others.


An AI-powered personal finance assistant focused on:

- Expense tracking
- Shared expense management
- Reimbursements
- Investment tracking
- Monthly financial insights

------------
## Problem Statement

I invest a significant portion of my income every month, but I often struggle to answer simple questions such as:
- How much did I spend on food this month?
- How much did I spend shopping?
- How much money am I waiting to get back from friends?
- Where is my money actually going?

Traditional expense tracking becomes difficult because:
- Credit card statements contain both personal and shared expenses
- Splitwise entries are easy to forget
- Expense categorization requires manual effort
- Spending insights are scattered across multiple tools

This project aims to solve those problems by building a personal financial assistant that automatically organizes, categorizes, and analyzes spending behavior.

------------------

# Current Features

## Transaction Management

- Create transactions
- Store merchant information
- Track payment sources
- Categorize expenses
- Add notes and metadata

## Split Expense Tracking

- Split transactions among multiple participants
- Validate split allocations
- Track reimbursements
- Mark transactions as split expenses

## Dashboard Analytics

- Personal spend this month
- Investments this month
- Money owed to me
- Total transaction count
- Split transaction count

## Financial Rules

- Investments are tracked separately from spending
- Personal spend includes only the current month's expenses
- Outstanding reimbursements remain visible until received
- Split allocations must equal the original transaction amount

-------------------

# Architecture

```text
Streamlit Frontend (Planned)
            ↓
      FastAPI Backend
            ↓
       Service Layer
            ↓
   Supabase (PostgreSQL)
```

## API Layer

Responsible for:

- Receiving requests
- Validating payloads
- Routing requests to services
- Returning responses

```text
api/
├── transactions.py
├── dashboard.py
```

## Service Layer

Responsible for:

- Business logic
- Financial calculations
- Data validation
- Database operations

```text
services/
├── transaction_service.py
├── split_service.py
├── dashboard_service.py
```

## Schema Layer

Responsible for:

- Request validation
- Response validation
- Type safety
- Automatic API documentation

```text
schemas/
```

## Database Layer

### transactions

Stores all expense and investment records.

| Column | Description |
|----------|-------------|
| id | Transaction ID |
| transaction_date | Date of transaction |
| merchant | Merchant name |
| amount | Transaction amount |
| category | Expense category |
| payment_source | Payment method |
| notes | Additional notes |
| is_split | Indicates whether the transaction is shared |

### split_participants

Stores participant allocations for shared expenses.

| Column | Description |
|----------|-------------|
| transaction_id | Parent transaction |
| participant_name | Participant name |
| amount | Participant share |
| is_me | Whether participant is the user |
| reimbursement_received | Whether payment has been received |

---

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic

### Database

- Supabase
- PostgreSQL

### Frontend ( Planned )

- Streamlit

---

# API Endpoints

## Transactions

### Get All Transactions

```http
GET /transactions
```

### Create Transaction

```http
POST /transactions
```

## Split Expenses

### Create Transaction Split

```http
POST /transactions/{transaction_id}/split
```

## Dashboard

### Get Dashboard Summary

```http
GET /dashboard/summary
```

---

# Example Dashboard Response

```json
{
  "personal_spend_this_month": 11757,
  "investments_this_month": 25000,
  "money_owed_to_me": 9000,
  "transaction_count": 14,
  "split_transaction_count": 3
}
```

---

# Project Roadmap

## Sprint 1 - Complete

- Backend setup
- Supabase integration
- Transaction APIs

## Sprint 2 - Complete

- Split expense management
- Reimbursement tracking

## Sprint 3 - Complete

- Dashboard analytics
- Financial summaries
- Architecture cleanup

## Sprint 4 (In Progress)

- Merchant memory engine
- Automatic categorization
- Historical learning

---

# Future Enhancements

## Statement Import

- HDFC credit card statement parsing
- Bank statement ingestion
- Automatic transaction creation

## AI Categorization

- Learn merchant-category mappings
- Auto-suggest categories
- Confidence scoring

## Financial Insights

- Spending trends
- Monthly reports
- Category-wise analysis
- Budget tracking

## Personal Expense Tracking Features

- Cashflow insights
- Net worth tracking
- Goal tracking
- Investment analytics

---

# Running Locally

## Clone Repository

```bash
git clone https://github.com/anishkabhatia/personal-expense-tracker.git
cd personal-expense-tracker
```

## Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_role_key
```

## Start Backend

```bash
uvicorn app.main:app --reload
```

## API Documentation

Open:

```text
http://localhost:8000/docs
```

---

# Why I Built This

This project started as a personal problem.

I wanted a system that could automatically understand where my money goes, distinguish between personal and shared expenses, track reimbursements, and eventually act as a personal financial assistant.

Along the way, it has also become a practical way to learn backend engineering, API design, database modeling, and AI-powered financial workflows.