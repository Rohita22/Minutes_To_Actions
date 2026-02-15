import sqlite3
import json
from datetime import datetime, UTC

DB_NAME = "minutestoactions.db"

#will directly be created in folder; SQLite is file based so no seperate db server needed
#sqlite3 is python built in version of sqlite
def get_connection():
    conn = sqlite3.connect(DB_NAME) #conn is active connection to db
    conn.row_factory = sqlite3.Row #changes how defalt query results returned as sqlite returns tuples
    #this line basically lets is return like row["title"] instead of row[0]
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor() #cursor runs the db

    # Create sessions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        notes TEXT,
        summary_json TEXT,
        decisions_json TEXT,
        created_at TEXT
    )
    """)

    # Create action_items table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS action_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER,
        owner TEXT,
        task TEXT,
        due_date TEXT,
        priority TEXT,
        FOREIGN KEY(session_id) REFERENCES sessions(id) 
    )
    """)
#foreign key ensures that the session id in action_items table reference to the one in session tb, so that
#cannot create a task for a session id that doesn't exist
    conn.commit()
    conn.close()

def insert_session(title: str, notes: str, summary: list, decisions: list, action_items: list) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    created_at = datetime.now(UTC).isoformat()

    cursor.execute(
        """
        INSERT INTO sessions (title, notes, summary_json, decisions_json, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (title, notes, json.dumps(summary), json.dumps(decisions), created_at),
    )
    session_id = cursor.lastrowid

    for item in action_items:
        cursor.execute(
            """
            INSERT INTO action_items (session_id, owner, task, due_date, priority)
            VALUES (?, ?, ?, ?, ?)
            """,
            (session_id, item["owner"], item["task"], item.get("due_date"), item["priority"]),
        )

    conn.commit()
    conn.close()
    return session_id


def list_sessions():
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        "SELECT id, title, created_at, summary_json FROM sessions ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return rows


def get_session(session_id: int):
    import json
    conn = get_connection()
    cursor = conn.cursor()

    session_row = cursor.execute(
        "SELECT * FROM sessions WHERE id = ?", (session_id,)
    ).fetchone()

    if not session_row:
        conn.close()
        return None

    items = cursor.execute(
        "SELECT owner, task, due_date, priority FROM action_items WHERE session_id = ?",
        (session_id,),
    ).fetchall()

    conn.close()

    return {
        "id": session_row["id"],
        "title": session_row["title"],
        "notes": session_row["notes"],
        "created_at": session_row["created_at"],
        "summary": json.loads(session_row["summary_json"] or "[]"),
        "decisions": json.loads(session_row["decisions_json"] or "[]"),
        "action_items": [dict(i) for i in items],
    }
