import sqlite3
import pandas as pd

def setup_database():
    conn = sqlite3.connect("database/regulatory.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            account TEXT,
            type TEXT,
            amount REAL,
            transaction_date TEXT
        )
    """)

    # Create audit log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_month TEXT,
            generated_at TEXT,
            status TEXT
        )
    """)

    # Load CSV into table
    df = pd.read_csv("data/transactions.csv")
    df.to_sql("transactions", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()

    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()