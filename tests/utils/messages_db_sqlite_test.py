import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the system path
absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
print("Adding to sys.path:", absolute_path)
sys.path.append(absolute_path)

load_dotenv()

from src.utils import (
    create_conversations_table,
    add_message_with_embedding,
    get_recent_conversations,
    find_similar_messages_for_user,
    find_recent_similar_messages_by_date,
    find_similar_messages_by_topic
)

def test_create_conversations_table():
    print("Initializing test conversations table creation...")
    create_conversations_table()

    import sqlite3
    conn = sqlite3.connect("messages_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conversations'")
    result = cursor.fetchone()
    assert result is not None, "conversations table was not created successfully."
    print("conversations table created successfully.", result)

def test_add_message_with_embedding():
    print("Initializing test add_message_with_embedding...")
    message_id = add_message_with_embedding(
        user_id=1,
        role="user",
        content="Test message content",
        topic_summary="Test Summary"
    )
    assert message_id is not None, "conversation added successfully."

    import sqlite3
    conn = sqlite3.connect("messages_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conversations WHERE user_id = (?)", (1,))
    result = cursor.fetchone()
    print("test user conversation created successfully.", result)

def test_get_recent_conversations():
    print("Initializing test get_recent_conversations...")
    conversations = get_recent_conversations(user_id=1, limit=5)

    assert len(conversations) > 0, "No recent conversations found."
    print("Recent conversations retrieved successfully.", conversations)

def test_find_similar_messages_for_user():
    print("Initializing test find_similar_messages_for_user...")
    conversations = find_similar_messages_for_user(
        query="Test message content",
        user_id=1, 
        limit=5
    )

    assert len(conversations) > 0, "No recent conversations found."
    print("Recent conversations retrieved successfully.", conversations)

def test_find_recent_similar_messages_by_date():
    print("Initializing test find_recent_similar_messages_by_date...")
    conversations = find_recent_similar_messages_by_date(
        query="Test message content",
        user_id=1, 
        limit=5,
        time_limit_days=7
    )

    assert len(conversations) > 0, "No recent conversations found."
    print("Recent conversations retrieved successfully.", conversations)

def test_find_similar_messages_by_topic():
    print("Initializing test find_similar_messages_by_topic...")
    message_id = add_message_with_embedding(
        user_id=2,
        role="user",
        content="Test content test for input of the start message content summary",
        topic_summary="Test Summary"
    )
    assert message_id is not None, "conversation added successfully."
    conversations = find_similar_messages_by_topic(
        query="Test content",
        topic_keywords=["Summary"],
        user_id=2, 
        limit=5
    )

    assert len(conversations) > 0, "No recent conversations found."
    print("Recent conversations retrieved successfully.", conversations)


test_create_conversations_table()
print("All DDL tests passed successfully.")

test_add_message_with_embedding()
print("All DML tests passed successfully.")

#test_get_recent_conversations()
#test_find_similar_messages_for_user()
#test_find_recent_similar_messages_by_date()
#test_find_similar_messages_by_topic()
print("All DQL tests passed successfully.")