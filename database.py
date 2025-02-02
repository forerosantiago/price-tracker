"""
This module sets up the database schema for the price tracker application.
"""

import sqlite3

def connect_to_db():
    """Connects to the SQLite database."""
    return sqlite3.connect('test.db')

def execute_query(query, params=None):
    """Executes an SQL query."""
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query, params or [])
    conn.commit()
    conn.close()

execute_query('''
CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
''')

execute_query('''
CREATE TABLE IF NOT EXISTS Stores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    url TEXT UNIQUE
)
''')

execute_query('''
CREATE TABLE IF NOT EXISTS ProductStore (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER REFERENCES Products(id),
    store_id INTEGER REFERENCES Store(id),
    name TEXT,
    url TEXT UNIQUE,
    last_price REAL,
    UNIQUE(product_id, store_id)
)
''')

execute_query('''
CREATE TABLE IF NOT EXISTS PriceHistory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_store_id INTEGER REFERENCES ProductStore(id),
    price REAL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
