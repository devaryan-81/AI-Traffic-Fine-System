# database_manager.py
# Handles SQLite database operations for storing violation records

import sqlite3
import os
from datetime import datetime

# Ensure the /database/ folder exists
os.makedirs("database", exist_ok=True)

# Connect to SQLite database (will create if it doesn't exist)
conn = sqlite3.connect("database/violations.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS violations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_number TEXT,
        violation_type TEXT,
        timestamp TEXT
    )
''')
conn.commit()

def insert_violation_record(vehicle_number, violation_type):
    """
    Inserts a new violation record into the database.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO violations (vehicle_number, violation_type, timestamp)
        VALUES (?, ?, ?)
    ''', (vehicle_number, violation_type, timestamp))
    conn.commit()
    print(f"[DB] Logged: {vehicle_number} - {violation_type} at {timestamp}")
