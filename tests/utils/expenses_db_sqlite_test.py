import os 
import sys

from src.utils.expenses_db_sqlite  import create_expenses_table, cursor


# Test the database connection and table creation
def test_create_expenses_table():
    print("Initializing test database...")
    create_expenses_table()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='expenses'")
    result = cursor.fetchone()
    assert result is not None, "Expenses table was not created successfully."
    print("Expenses table created successfully.")

# Test the database connection and creation 
test_create_expenses_table()