import sqlite3

def create_progress_table():
    conn = sqlite3.connect("db/user_data.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            username TEXT,
            topic TEXT,
            q_type TEXT,
            score INTEGER,
            total INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_progress(username, topic, q_type, score, total):
    conn = sqlite3.connect("db/user_data.db")
    c = conn.cursor()
    c.execute("INSERT INTO progress (username, topic, q_type, score, total) VALUES (?, ?, ?, ?, ?)",
              (username, topic, q_type, score, total))
    conn.commit()
    conn.close()

def get_user_progress(username):
    conn = sqlite3.connect("db/user_data.db")
    c = conn.cursor()
    c.execute("SELECT topic, q_type, score, total FROM progress WHERE username=?", (username,))
    data = c.fetchall()
    conn.close()
    return data
