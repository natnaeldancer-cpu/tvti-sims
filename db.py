import sqlite3
import os

folder = os.path.expanduser("~/TVTI_SIMS")
os.makedirs(folder, exist_ok=True)
file = os.path.join(folder, "tvti.db")

session = {"user": ""}

def connect():
    db = sqlite3.connect(file)
    db.execute("""CREATE TABLE IF NOT EXISTS users (
 username TEXT PRIMARY KEY,
password TEXT NOT NULL)""")
    db.execute("""CREATE TABLE IF NOT EXISTS students (
 student_id TEXT PRIMARY KEY,
full_name TEXT NOT NULL,
 gender TEXT,
 age INTEGER,
department TEXT,
level TEXT,
phone TEXT,
semester TEXT DEFAULT '',
gpa REAL DEFAULT 0)""")
    db.execute("INSERT OR IGNORE INTO users VALUES ('admin', 'admin123')")
    db.commit()
    return db