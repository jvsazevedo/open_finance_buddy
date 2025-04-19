from typing import Dict, Any

mothly_income = {
    "currency": "BRL",
    "amount": 7500.00,
}

expenses = [
    {
        "year": 2025,
        "month": 2,
        "expenses": [
            {
                "name": "Rent",
                "amount": 1000,
                "recurrence": "monthly",
            },
            {
                "name": "Groceries",
                "amount": 500,
                "recurrence": "weekly",
            },
            {
                "name": "Transport",
                "amount": 200,
                "recurrence": "monthly",
            },
            {
                "name": "Entertainment",
                "amount": 300,
                "recurrence": "monthly",
            },
        ]
    },
    {
        "year": 2025,
        "month": 1,
        "expenses": [
            {
                "name": "Rent",
                "amount": 1000,
                "recurrence": "monthly",
            },
            {
                "name": "Groceries",
                "amount": 500,
                "recurrence": "weekly",
            },
            {
                "name": "Transport",
                "amount": 200,
                "recurrence": "monthly",
            }
        ]
    }
]

def get_user_monthly_income(user_id):
    """
    Fetch the monthly income of a user from the database.
    
    Args:
        user_id (int): The ID of the user.

    Returns:
        Dict: The monthly income of the user and the currency.
    """
    return mothly_income

def get_user_monthly_expenses(user_id):
    """
    Fetch the monthly expenses of a user from the database.
    
    Args:
        user_id (int): The ID of the user.

    Returns:
        List[Dict]: The monthly expenses of the user.
    """
    return expenses

def get__expenses_by_month(user_id: str, month: int):
    """
    Fetch the expenses of a user for a specific month from the database.
    
    Args:
        user_id (str): The ID of the user.
        month (int): The month for which to fetch expenses.

    Returns:
        List[Dict]: The expenses of the user for the specified month.
    """
    for expense in expenses:
        if expense["month"] == month:
            return expense["expenses"]
    return []

def add_user_expense(user_id: str, month: int, expense: Dict[str, Any]):
    """
    Add an expense for a user for a specific month to the database.
    
    Args:
        user_id (str): The ID of the user.
        month (int): The month for which to add the expense.
        expense (Dict[str, Any]): The expense to add.

    Returns:
        None
    """
    for exp in expenses:
        if exp["month"] == month:
            exp["expenses"].append(expense)
            return
    expenses.append({"year": 2025, "month": month, "expenses": [expense]})