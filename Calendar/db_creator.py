import sqlite3
import random as ran
import time
from datetime import timedelta
import radar

names = [
    "Ralvenom", "Andmos", "Caslius", "Mavichar", "Ben", "Uka",
    "Gad", "Lezu", "Wrerick Thundertwist", "Almin Salwuners",
    "Lilnise", "Inlies", "Yoraborys", "Nerali", "Zenise", "Ariayola",
    "Ariamine", "Agnelia", "Rogrea", "Yayola", "Psalm", "Fresh", "Immortal",
    "Virtue", "Journey", "Relentless", "Despair", "Hope", "Chant"
]

pending_s = ["a", "b", "c"]

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

ran.seed(time.time())

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT,
    age         INTEGER,
    date_added  TEXT,
    deadline    TEXT,
    pending     TEXT
)
""")

cursor.execute("DELETE FROM users")  # reset data (optional)

for name in names:
    dt = radar.random_datetime()
    date = dt.strftime("%d-%m-%Y")

    dl = dt + timedelta(days=30)
    deadline = dl.strftime("%d-%m-%Y")

    pend = ", ".join(ran.choices(pending_s, k=ran.randint(1, 3)))

    cursor.execute(
        "INSERT INTO users (name, age, date_added, deadline, pending) VALUES (?, ?, ?, ?, ?)",
        (name, ran.randint(10, 70), date, deadline, pend)
                )


conn.commit()
conn.close()