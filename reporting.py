import sqlite3

def generate_monthly_report():
    conn = sqlite3.connect("database/regulatory.db")
    cursor = conn.cursor()

    query = """
        SELECT 
            strftime('%Y-%m', transaction_date) AS reporting_month,
            type,
            SUM(amount) AS total_amount,
            COUNT(*) AS transaction_count
        FROM transactions
        GROUP BY reporting_month, type
    """

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    return results
