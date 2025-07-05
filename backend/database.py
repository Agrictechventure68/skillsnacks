import sqlite3

def init_db():
    conn = sqlite3.connect('skillsnacks.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            phone TEXT NOT NULL,
            last_lesson INTEGER DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()
