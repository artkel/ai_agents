import sqlite3
import os


def reset_database():
    """Empty the fashion trends database by deleting and recreating it."""
    db_path = 'fashion_trends.db'

    # Close any existing connections
    try:
        conn = sqlite3.connect(db_path)
        conn.close()
    except:
        pass

    # Delete the database file if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Database '{db_path}' has been deleted.")
    else:
        print(f"Database '{db_path}' does not exist or has already been deleted.")

    # Create a fresh database with the schema
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the trends table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trends (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trend_name TEXT UNIQUE NOT NULL,
        source_url TEXT NOT NULL,
        discovered_date TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

    print(f"A fresh database has been created at '{db_path}'.")


# Run the function
if __name__ == "__main__":
    reset_database()