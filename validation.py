import sqlite3

def run_validation():
    conn = sqlite3.connect("database/regulatory.db")
    cursor = conn.cursor()

    query = """
        SELECT * FROM transactions
        WHERE amount <= 0
        OR transaction_date IS NULL
        OR type NOT IN ('CREDIT','DEBIT')
        OR account IS NULL
    """

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    if results:
        print("Validation FAILED.")
        return False
    else:
        print("Validation PASSED.")
        return True
