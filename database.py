import sqlite3

def create_db():
    conn = sqlite3.connect("docify.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        content TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_document(filename, content):
    conn = sqlite3.connect("docify.db")
    cursor = conn.cursor()

    # normal table
    cursor.execute("""
    INSERT INTO documents (filename, content)
    VALUES (?, ?)
    """, (filename, content))

    # FTS table
    cursor.execute("""
    INSERT INTO documents_fts (filename, content)
    VALUES (?, ?)
    """, (filename, content))

    conn.commit()
    conn.close()


def create_fts_table():
    conn = sqlite3.connect("docify.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts
    USING fts5(filename, content)
    """)

    conn.commit()
    conn.close()


create_db()
create_fts_table()