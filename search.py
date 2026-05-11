import sqlite3

def search_documents(keyword):
    conn = sqlite3.connect("docify.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT filename, content
    FROM documents_fts
    WHERE documents_fts MATCH ?
    """, (keyword,))

    results = cursor.fetchall()
    conn.close()

    return results