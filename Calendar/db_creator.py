import sqlite3
import random as ran
import time
from datetime import timedelta
import radar
from pathlib import Path

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

pending_s = ["υλικά", "πάγκος", "συσκευές"]


db_path = Path.home() / "desktop" / "KITCHEN" / "Kitchen_Design_Helper" / "Calendar" / "test.db"
db_path.parent.mkdir(exist_ok=True)

conn = sqlite3.connect(str(db_path))

cursor = conn.cursor()

ran.seed(time.time())

cursor.execute("""
CREATE TABLE IF NOT EXISTS kitchens (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    client              TEXT,
    designer            TEXT,
    analysis_date       TEXT,
    certification_date  TEXT,
    pending             TEXT
)
""")

cursor.execute("DELETE FROM kitchens")  # reset data (optional)

for name in names:
    an = radar.random_datetime()
    # analysis = an.strftime("%d-%m-%Y") PROBLEMS WITH FILTERING DATES
    analysis = an.strftime("%Y-%m-%d")

    crt = an + timedelta(days=30)
    # certification = crt.strftime("%d-%m-%Y") PROBLEMS WITH FILTERING DATES
    certification = crt.strftime("%Y-%m-%d")

    pend = ", ".join(ran.choices(pending_s, k=ran.randint(1, 3)))

    des = ran.choice(desgn)

    checklst = ran.choice([0, 1])

    cursor.execute(
        """INSERT INTO kitchens (client, designer, analysis_date, certification_date, pending) 
            VALUES (?, ?, ?, ?, ?)""",
            (name, des, analysis, certification, pend)
                )


conn.commit()
conn.close()