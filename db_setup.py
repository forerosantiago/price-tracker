import sqlite3

def initialize_database():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()

        # Create Stores table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Stores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            url TEXT UNIQUE)
        """)
        
        # Create Products table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            image_url TEXT)
        """)

        # Create ProductStores table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ProductStores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER REFERENCES Products(id) ON DELETE CASCADE,
            store_id INTEGER REFERENCES Stores(id) ON DELETE CASCADE,
            name TEXT,
            url TEXT UNIQUE,
            last_price REAL)
        """)

        # Create PriceHistory table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS PriceHistory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_store_id INTEGER REFERENCES ProductStores(id) ON DELETE CASCADE,
            price REAL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        """)

        # Add supported stores into the Stores table
        conn.execute("INSERT OR IGNORE INTO Stores (name, url) VALUES (?, ?)",
            ("Exito", "https://www.exito.com/") 
        )

        conn.execute("INSERT OR IGNORE INTO Stores (name, url) VALUES (?, ?)",
            ("Carulla", "https://www.carulla.com/")
        )

        conn.execute("INSERT OR IGNORE INTO Stores (name, url) VALUES (?, ?)",
            ("Jumbo", "https://www.jumbo.com/")
        )

        conn.commit()

if __name__ == '__main__':
    initialize_database()
    print("Database initialized successfully.")