import sqlite3
import csv

conn = sqlite3.connect("baseball.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS batting_avg (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        League TEXT,
        Name TEXT,
        Team TEXT,
        Batting_Average REAL,
        Year INTEGER
    )
""")

with open("batting_avg.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row
    for row in reader:
        try:
            cursor.execute(
                "INSERT INTO batting_avg (League, Name, Team, Batting_Average, Year) VALUES (?, ?, ?, ?, ?)",
                (row[1], row[2], row[3], row[4], row[5])
            )
        except Exception as e:
            print(f"Error inserting row {row}: {e}")
        
        
cursor.execute("""
    CREATE TABLE IF NOT EXISTS home_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Career_Home_Runs INTEGER
    )
""")

with open("home_runs.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        try:
             cursor.execute(
                "INSERT INTO home_runs (Name, Career_Home_Runs) VALUES (?, ?)",
                (row[1], row[2])
            )
        except Exception as e:
            print(f"Error inserting row {row}: {e}")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS career_strikeouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        League TEXT,
        Name TEXT,
        Career_Strikeouts INTEGER
    )
""")

with open("career_strikeouts.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if not row:
            continue
        if len(row) < 4:
            print("Skipping malformed row:", row)
            continue
        
        try:
            cursor.execute(
                "INSERT INTO career_strikeouts (League, Name, Career_Strikeouts) VALUES (?, ?, ?)",
                (row[1], row[2], row[3])
            )
        except Exception as e:
            print(f"Error inserting row {row}: {e}")
    
conn.commit()
conn.close()

print("All CSV files have been imported into baseball.db.")



