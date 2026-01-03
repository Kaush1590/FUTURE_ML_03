from pathlib import Path
import sqlite3

# Path to the history database file
HISTORY_DB = Path(__file__).parent / "db" / "chat_history.db"

# Create required folders for the history database
HISTORY_DB.parent.mkdir(parents = True, exist_ok = True)

# Create a connection to the history database
def get_connection():
    return sqlite3.connect(HISTORY_DB, check_same_thread = False)

# Initialize the history table if it does not exist
def database_init():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            session_name TEXT,
            role TEXT,
            content TEXT,
            timestamp TEXT,
            reaction TEXT
        )
    """)

    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_chat_session
        ON chat_history(session_id)
    """)

    conn.commit()
    conn.close()

# Load all messages for a given session
def load_chat(session_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, role, content, timestamp, reaction
        FROM chat_history
        WHERE session_id = ?
        ORDER BY id
    """, (session_id,))

    rows = cur.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "role": r[1],
            "content": r[2],
            "timestamp": r[3],
            "reaction": r[4]
        }
        for r in rows
    ]

# Save a single chat message to the database
def save_message(session_id, session_name, role, content, timestamp, reaction = None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO chat_history
        (session_id, session_name, role, content, timestamp, reaction)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (session_id, session_name, role, content, timestamp, reaction))

    conn.commit()
    conn.close()

# Update the user's reaction for a specific assistant message
def update_reaction(message_id, reaction):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE chat_history
        SET reaction = ?
        WHERE id = ?
    """, (reaction, message_id))

    conn.commit()
    conn.close()

# Delete all messages belonging to a session
def clear_history(session_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM chat_history
        WHERE session_id = ?
    """, (session_id,))

    conn.commit()
    conn.close()

# Fetch all existing chat sessions
def get_all_sessions():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT session_id, session_name
        FROM chat_history
        GROUP BY session_id
        ORDER BY MIN(id) DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows

# Rename an existing chat session
def rename_session(session_id, new_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE chat_history
        SET session_name = ?
        WHERE session_id = ?
    """, (new_name, session_id))

    conn.commit()
    conn.close()

# Automatically name a session using the first user message
def auto_name_session(session_id, message, max_len = 40):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT session_name
        FROM chat_history
        WHERE session_id = ?
        LIMIT 1
    """, (session_id,))

    row = cur.fetchone()
    if row and row[0] in ("New chat", "Untitled chat"):
        title = message.strip().split("\n")[0][:max_len]
        cur.execute("""
            UPDATE chat_history
            SET session_name = ?
            WHERE session_id = ?
        """, (title, session_id))

    conn.commit()
    conn.close()