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
    name TEXT UNIQUE,
    image_url TEXT
)
''')

# create sample product
execute_query('''
INSERT OR IGNORE INTO Products (name, image_url) VALUES
            ('Apple', 'https://th.bing.com/th?id=OSK.ltvSJTmoyE5rpGQvfAlGoYLWlGWItpzKQQ6H0tfAFPg&w=224&h=200&c=12&rs=1&r=0&o=6&pid=SANGAM'),
            ('Banana', 'https://www.bing.com/th?id=OIP.rYDhN8E1MHf6oE63MM9C-wHaFj&w=248&h=185&c=8&rs=1&qlt=90&r=0&o=6&pid=3.1&rm=2'),
            ('Orange', 'https://th.bing.com/th/id/OIP.JHF15LJdaA9X_lVGaquRTQHaE8?rs=1&pid=ImgDetMain')
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
