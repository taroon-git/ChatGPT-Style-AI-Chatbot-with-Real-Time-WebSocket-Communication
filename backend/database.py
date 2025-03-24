import mysql.connector
from mysql.connector import Error, pooling
import os
from dotenv import load_dotenv
import uuid
from typing import List, Dict, Optional
from datetime import datetime

# Load environment variables
load_dotenv()

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "chatbot_db")

# Connection pool configuration
dbconfig = {
    "host": DB_HOST,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME
}

# Create a connection pool
connection_pool = pooling.MySQLConnectionPool(
    pool_name="chatbot_pool",
    pool_size=5,  # Adjust based on your needs
    **dbconfig
)

def get_db_connection():
    """
    Establish a connection to the MySQL database using a connection pool.
    """
    try:
        connection = connection_pool.get_connection()
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise


# 🔹 Create a new session & return session_id
def create_session():
    session_id = str(uuid.uuid4())  # Generate unique session ID
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_sessions (session_id) VALUES (%s)", (session_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return session_id  # Return the generated session_id

# 🔹 Save messages to database
def save_message(session_id, message, role):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_messages (session_id, message, role, timestamp) VALUES (%s, %s, %s, %s)",
        (session_id, message, role, datetime.now()),
    )
    conn.commit()
    cursor.close()
    conn.close()

# 🔹 Retrieve chat history for a session
def get_chat_history(session_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT role, message FROM chat_messages WHERE session_id = %s", (session_id,))
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return messages  # List of messages


def create_new_session():
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()

    session_id = f"session_{int(datetime.now().timestamp())}"  # Unique session ID
    cursor.execute("INSERT INTO chat_sessions (session_id, created_at) VALUES (%s, %s)", (session_id, datetime.now()))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return session_id