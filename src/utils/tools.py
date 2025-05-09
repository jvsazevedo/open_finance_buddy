from typing import Dict, Any
from langchain_core.tools import tool

import sys
import os

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from utils.expenses_db_sqlite import (
    get_user_monthly_income,
    get_user_monthly_expenses,
    get_expenses_by_month,
    add_user_expense
)
# Importing message-related utilities for future use


@tool
def search_user_monthly_income(user_id: str) -> Dict[str, Any]:
    """
    Search for the user's monthly income
    Use this tool to filter the income by month
    Params:
    - user_id: The user id
    """
    income = get_user_monthly_income(user_id)
    return income


@tool
def search_user_monthly_expenses(user_id: str) -> Dict[str, Any]:
    """
    Search for the user's expenses
    Use this tool to filter the expenses by month
    You should use this when user asks about expenses, or for making decisions about expenses
    For cases like if they can buy a new car or how much they can spend
    Params:
    - user_id: The user id
    """
    expenses = get_user_monthly_expenses(user_id)
    return expenses


@tool
def search_expense_by_month(user_id: str, month: int) -> Dict[str, Any]:
    """
    Search for the user's expenses by month
    Use this tool to filter the expenses by month
    Params:
    - user_id: The user id
    - month: The month to filter the income by (1-12)
    """
    expenses = get_expenses_by_month(user_id, month)
    return expenses


@tool
def add_user_expense_in_month(user_id: str, month: int,
                              expense: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add a new expense for the user
    Use this tool to add a new expense for the user
    Params:
    - user_id: The user id
    - month: The month to add expense (1-12), default to current month if not provided
    - expense: The expense to add
    """
    # Implement the logic to add the expense to the database
    add_user_expense(user_id, month, expense)
    return {"status": "success", "message": "Expense added successfully"}


@tool
def add_chat_message(user_id: str, message: str) -> Dict[str, Any]:
    """
    Add a chat message to the user's conversation history
    Use this tool to add a chat message to the user's conversation history
    Params:
    - user_id: The user id
    - message: The message to add
    """
    # Implement the logic to add the message to the database or conversation history
    pass


tools = [
    search_user_monthly_income,
    search_user_monthly_expenses,
    search_expense_by_month,
    add_user_expense_in_month
]
