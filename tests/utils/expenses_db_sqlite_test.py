import os
import sys

# Add the parent directory to the system path
absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
print("Adding to sys.path:", absolute_path)

sys.path.append(absolute_path)

from src.utils  import create_expenses_table, create_user_table, create_user_params_table, add_user

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

    print("User ID:", user_id)
    print("User id type:", type(user_id))

    import sqlite3
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE id = ?", (user_id))
    result = cursor.fetchone()
    assert result is not None, "user table was not created successfully."
    print("test user created successfully.", result)

test_create_expenses_table()
test_create_users_table()
test_create_user_params_table()
print("All DDL tests passed successfully.")

test_add_user()
print("All DML tests passed successfully.")

