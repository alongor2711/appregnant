import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "pregnancy"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "postgres"),
    )


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS ingredients (
                    id     SERIAL PRIMARY KEY,
                    name   TEXT UNIQUE NOT NULL,
                    status TEXT NOT NULL,
                    notes  TEXT DEFAULT ''
                )
            """)


def get_all_ingredients():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT name, status, notes FROM ingredients ORDER BY name")
            return cur.fetchall()


def check_ingredients(text):
    names = [i.strip().lower() for i in text.split(",") if i.strip()]
    results = []
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            for name in names:
                cur.execute(
                    "SELECT status, notes FROM ingredients WHERE name = %s",
                    (name,)
                )
                row = cur.fetchone()
                if row:
                    results.append({
                        "name": name.title(),
                        "status": row["status"],
                        "notes": row["notes"]
                    })
                else:
                    results.append({
                        "name": name.title(),
                        "status": "Unknown",
                        "notes": "Not in database"
                    })
    return results


def add_ingredient(name, status, notes=""):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO ingredients (name, status, notes)
                VALUES (%s, %s, %s)
                ON CONFLICT (name) DO UPDATE SET status = EXCLUDED.status, notes = EXCLUDED.notes
                """,
                (name.strip().lower(), status.strip(), notes.strip())
            )


def delete_ingredient(name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM ingredients WHERE name = %s", (name.strip().lower(),))
