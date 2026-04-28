import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    date TEXT
)
""")

cursor.execute("DELETE FROM users")  # reset data (optional)

cursor.executemany(
    "INSERT INTO users (name, age, date) VALUES (?, ?, ?)",
    [
        ("Alice", 24, "23-05-2020"),
        ("Bob", 30, "13-11-2025"),
        ("Charlie", 28, "27-1-2001")
    ]
)

conn.commit()
conn.close()