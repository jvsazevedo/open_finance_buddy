from typing import Dict, Any
import sqlite3
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()


def create_expenses_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        label TEXT,
        value REAL,
        currency TEXT,
        recurrent INTEGER,
        installments INTEGER,
        expiring_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()


def create_user_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        password TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        deleted_at TIMESTAMP DEFAULT NULL
    )
    """)
    conn.commit()


def create_user_params_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_params (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        label TEXT,
        value TEXT
    )
    """)
    conn.commit()

def initialize_database():
    """
    Initialize the database by creating the necessary tables.
    This function should be called once to set up the database schema.
    """
    create_expenses_table()
    create_user_table()
    create_user_params_table()

def get_user_monthly_income(user_id: int) -> float | None:
    """
    Fetch the monthly income of a user from the database.

    Args:
        user_id (int): The ID of the user.

    Returns:
        Dict: The monthly income of the user and the currency.
    """
    cursor.execute(
        """
        SELECT value FROM user_params
        WHERE user_id = ? AND label = 'monthly_income'
        ORDER BY id DESC
        LIMIT 1
        """,
        [user_id]
    )
    result = cursor.fetchone()

    return float(result[0]) if result else None


def get_recent_user_expenses(user_id: int) -> list[Dict[str, Any]]:
    """
    Fetch 50 recent user expenses from the database.

    Args:
        user_id (int): The ID of the user.

    Returns:
        List[Dict]: The monthly expenses of the user.
    """
    cursor.execute(
        """
        SELECT * FROM expenses
        WHERE user_id = ?
        ORDER BY expiring_date DESC
        LIMIT 50
        """,
        (user_id,)
    )
    result = cursor.fetchall()
    print("Recent user expenses fetched:", result)
    if not result:
        return []
    return result


def get_expenses_by_month(user_id: int, month: int) -> list[Dict[str, Any]]:
    """
    Fetch the expenses of a user for a specific month from the database.

    Args:
        user_id (str): The ID of the user.
        month (int): The month for which to fetch expenses.

    Returns:
        List[Dict]: The expenses of the user for the specified month.
    """
    cursor.execute(
        """
        SELECT * FROM expenses
        WHERE user_id = ? AND strftime('%m', expiring_date) = ?
        ORDER BY expiring_date DESC
        LIMIT 50
        """,
        (user_id, str(month).zfill(2))
    )
    result = cursor.fetchall()

    return result


def add_user_expense(user_id: int, expense: Dict[str, Any]):
    """
    Add an expense for a user for a specific month to the database.

    Args:
        user_id (str): The ID of the user.
        expense (Dict[str, Any]): The expense to add.

    Returns:
        None
    """
    cursor.execute(
        """
        INSERT INTO expenses (
            user_id,
            label,
            value,
            currency,
            recurrent,
            installments,
            expiring_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            expense["label"],
            expense["value"],
            expense["currency"],
            expense["recurrent"],
            expense["installments"],
            expense["expiring_date"] if "expiring_date" in expense else None
        )
    )
    conn.commit()
    return cursor.lastrowid


def add_user(user: Dict[str, Any]):
    """
    Add a user to the database.

    Args:
        user (Dict[str, Any]): The user to add.

    Returns:
        the ID of the user.
    """
    cursor.execute(
        "INSERT INTO user (name, email, password) VALUES (?, ?, ?)",
        (
            user["name"],
            user["email"],
            user["password"]
        )
    )
    conn.commit()
    return cursor.lastrowid


def add_user_param(user_id: int, param: Dict[str, Any]):
    """
    Add a user parameter to the database.

    Args:
        user_id (int): The ID of the user.
        param (Dict[str, Any]): The parameter to add.

    Returns:
        the ID of the parameter.
    """
    cursor.execute(
        "INSERT INTO user_params (user_id, label, value) VALUES (?, ?, ?)",
        (
            user_id,
            param["label"],
            param["value"]
        )
    )
    conn.commit()
    return cursor.lastrowid
