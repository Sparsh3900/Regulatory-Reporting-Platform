import sqlite3
from datetime import datetime

def detect_breach_and_log(report_data):
    conn = sqlite3.connect("database/regulatory.db")
    cursor = conn.cursor()

    for row in report_data:
        month, type_, total, count = row

        status = "OK"
        if total > 100000:
            status = "BREACH"

        cursor.execute("""
            INSERT INTO audit_log (report_month, generated_at, status)
            VALUES (?, ?, ?)
        """, (month, datetime.now(), status))

    conn.commit()
    conn.close()
