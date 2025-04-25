import os
import sys

# Add the parent directory to the system path
absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
print("Adding to sys.path:", absolute_path)

sys.path.append(absolute_path)

from src.utils import (
    create_expenses_table,
    create_user_table,
    create_user_params_table,
    add_user,
    add_user_param,
    add_user_expense,
    get_user_monthly_income,
    get_user_monthly_expenses,
    get_expenses_by_month
)


def test_create_expenses_table():
    print("Initializing test expense table creation...")
    create_expenses_table()

    import sqlite3
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='expenses'")
    result = cursor.fetchone()
    assert result is not None, "expenses table was not created successfully."
    print("expenses table created successfully.", result)


def test_create_users_table():
    print("Initializing test users table creation...")
    create_user_table()

    import sqlite3
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
    result = cursor.fetchone()
    assert result is not None, "user table was not created successfully."
    print("user table created successfully.", result)


def test_create_user_params_table():
    print("Initializing test user params table creation...")
    create_user_params_table()

    import sqlite3
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_params'")
    result = cursor.fetchone()
    assert result is not None, "user_params table was not created successfully."
    print("user_params table created successfully.", result)


def test_add_user():
    print("Adding user to test database...")
    user_id = add_user({
        "name": "Test User",
        "email": "test_user@test.com",
        "password": "test_password"
    })

    import sqlite3
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE id = (?)", (user_id,))
    result = cursor.fetchone()
    assert result is not None, "user data was not inserted successfully."
    print("test user created successfully.", result)


def test_add_user_param():
    print("Adding user param to test database...")
    add_user_param(
        1,  # Assuming user_id 1 exists
        {
            "label": "monthly_income",
            "value": "7500.00"
        }
    )

    import sqlite3
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_params WHERE id = (?)", [1])
    result = cursor.fetchall()
    assert result is not None, "user_params data was not inserted successfully."
    print("test user param created successfully.", result)


def test_add_user_expense():
    print("Adding user expense to test database...")
    user_expense = add_user_expense(
        user_id=1,  # Assuming user_id 1 exists
        expense={
            "label": "Aluguel",
            "value": 650.00,
            "currency": "BRL",
            "recurrent": 1,
            "installments": 0,
            "expiring_date": "2025-04-25"
        }
    )

    import sqlite3
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id = (?)", [user_expense])
    result = cursor.fetchone()
    assert result is not None, "user_params data was not inserted successfully."
    print("test user param created successfully.", result)


def test_get_user_monthly_income():
    print("Getting user monthly income...")

    result = get_user_monthly_income(1)  # Assuming user_id 1 exists
    assert result is not None, "user monthly income was not retrieved successfully."
    print("User monthly income retrieved successfully.", result)


def test_get_user_monthly_expenses():
    print("Getting user monthly expenses...")

    result = get_user_monthly_expenses(1)  # Assuming user_id 1 exists
    assert result is not None, "user monthly expenses was not retrieved successfully."
    assert len(result) != 0, "user monthly expenses list is empty."
    print("User monthly expenses retrieved successfully.", result)


def test_get_expenses_by_month():
    print("Getting user expenses by month...")

    result = get_expenses_by_month(1, 5)  # Assuming user_id 1 exists
    assert result is not None, "user month expenses was not retrieved successfully."
    assert len(result) != 0, "user expenses by month list is empty."
    print("User expenses by month retrieved successfully.", result)


test_create_expenses_table()
test_create_users_table()
test_create_user_params_table()
print("All DDL tests passed successfully.")

test_add_user()
test_add_user_param()
test_add_user_expense()
print("All DML tests passed successfully.")

test_get_user_monthly_income()
test_get_user_monthly_expenses()
test_get_expenses_by_month()
print("All DQL tests passed successfully.")
