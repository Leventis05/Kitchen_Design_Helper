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

desgn = [
    "Thewraek stillmight", "Virgolor feathercrown",
    "Trakian boldgaze", "Ralofir oceancrown",
    "Farris nightsong", "Sylhorn irindromin",
    "Virmaer altont", "Ropeiros teliscophir",
    "Elqen custrahish", "Keanorin drathrerrann"
]

pending_s = ["a", "b", "c"]

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

ran.seed(time.time())

cursor.execute("""
CREATE TABLE IF NOT EXISTS kitchens (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    client          TEXT,
    designer        TEXT,
    analyses_date   TEXT,
    approval_date   TEXT,
    status          TEXT,
    pending         TEXT
)
""")

cursor.execute("DELETE FROM kitchens")  # reset data (optional)

for name in names:
    dt = radar.random_datetime()
    date = dt.strftime("%d-%m-%Y")

    dl = dt + timedelta(days=30)
    deadline = dl.strftime("%d-%m-%Y")

    pend = ", ".join(ran.choices(pending_s, k=ran.randint(1, 3)))

    des = ran.choice(desgn)

    cursor.execute(
        """INSERT INTO kitchens (client, designer, analyses_date, approval_date, status, pending) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (name, des, date, deadline, pend)
            )


conn.commit()
conn.close()