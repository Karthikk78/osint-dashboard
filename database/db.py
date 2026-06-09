import sqlite3


def init_db():

    conn = sqlite3.connect(
        "database/osint.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scans(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        domain TEXT,

        score INTEGER,

        risk_level TEXT,

        scan_date TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


def save_scan(
    domain,
    score,
    risk_level
):

    conn = sqlite3.connect(
        "database/osint.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO scans(
            domain,
            score,
            risk_level
        )

        VALUES(
            ?, ?, ?
        )
        """,
        (
            domain,
            score,
            risk_level
        )
    )

    conn.commit()
    conn.close()


def get_history():

    conn = sqlite3.connect(
        "database/osint.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
SELECT
    id,
    domain,
    score,
    risk_level,
    scan_date
FROM scans
ORDER BY id DESC
LIMIT 20
""")

    rows = cursor.fetchall()

    conn.close()

    return rows

def get_analytics():

    conn = sqlite3.connect(
        "database/osint.db"
    )

    cursor = conn.cursor()

    # Total scans
    cursor.execute(
        "SELECT COUNT(*) FROM scans"
    )

    total_scans = cursor.fetchone()[0]

    # Average score
    cursor.execute(
        "SELECT AVG(score) FROM scans"
    )

    avg_score = cursor.fetchone()[0]

    if avg_score is None:
        avg_score = 0

    # Risk counts

    cursor.execute("""
    SELECT
        risk_level,
        COUNT(*)

    FROM scans

    GROUP BY risk_level
    """)

    risk_data = cursor.fetchall()

    conn.close()

    return {
        "total_scans": total_scans,
        "avg_score": round(avg_score),
        "risk_data": risk_data
    }
def clear_history():

    conn = sqlite3.connect(
        "database/osint.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM scans"
    )

    conn.commit()
    conn.close()