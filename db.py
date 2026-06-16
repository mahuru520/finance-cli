import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "finance.db"

CATEGORIES = ["餐饮", "交通", "购物", "娱乐", "居住", "其他"]


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                amount  REAL NOT NULL,
                category TEXT NOT NULL,
                date    TEXT NOT NULL,
                note    TEXT DEFAULT ''
            )
        """)
        conn.commit()


def add_record(amount: float, category: str, date: str, note: str = ""):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO records (amount, category, date, note) VALUES (?, ?, ?, ?)",
            (amount, category, date, note),
        )
        conn.commit()


def query_records(
    year_month: str | None = None,
    categories: list[str] | None = None,
) -> list[dict]:
    sql = "SELECT * FROM records WHERE 1=1"
    params: list = []

    if year_month:
        sql += " AND date LIKE ?"
        params.append(f"{year_month}%")

    if categories:
        placeholders = ",".join("?" for _ in categories)
        sql += f" AND category IN ({placeholders})"
        params.extend(categories)

    sql += " ORDER BY date DESC"

    with get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()

    return [dict(r) for r in rows]


def get_record(record_id: int) -> dict | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM records WHERE id = ?", (record_id,)).fetchone()
    return dict(row) if row else None


def delete_record(record_id: int) -> bool:
    with get_conn() as conn:
        cursor = conn.execute("DELETE FROM records WHERE id = ?", (record_id,))
        conn.commit()
        return cursor.rowcount > 0


def get_stats(year_month: str | None = None) -> list[dict]:
    sql = """
        SELECT
            category,
            SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS income,
            SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) AS expense,
            COUNT(*) AS count
        FROM records
        WHERE 1=1
    """
    params: list = []

    if year_month:
        sql += " AND date LIKE ?"
        params.append(f"{year_month}%")

    sql += " GROUP BY category ORDER BY category"

    with get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()

    return [dict(r) for r in rows]
