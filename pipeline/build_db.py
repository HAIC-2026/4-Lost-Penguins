import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path("data/kyd.sqlite")
SCHEMA_PATH = Path("pipeline/schema.sql")

# 1. Start fresh: if an old database exists, delete it
if DB_PATH.exists():
    DB_PATH.unlink()
    print(f"Deleted old database at {DB_PATH}")
else:
    print(f"No old database found at {DB_PATH}. Starting fresh.")

# 2. Open the connection (this creates the file)
connection = sqlite3.connect(DB_PATH)

# 3. Turn on foreign-key checking (off by default in SQLite)
connection.execute("PRAGMA foreign_keys = ON")

# 4. Read schema.sql and run every command in it
connection.executescript(SCHEMA_PATH.read_text())

# 5. Insert one source (4 values: id, name, url, retrieved_at)
# use "?" instead of f-strings to avoid SQL injection attacks
# execute can only take one command at a time, so we can't use executescript here``
connection.execute(
    "INSERT INTO sources VALUES (?, ?, ?, ?)",
    ("acs5_2024", "ACS 5-year 2020-2024", "https://api.census.gov", "2026-11-09"),
)

# 6. Insert one metric (6 values: metric_id, label, unit, source_id, source_table, alias)
connection.execute(
    "INSERT INTO metrics VALUES (?, ?, ?, ?, ?, ?)",
    ("poverty_rate", "Poverty Rate", "%", "acs5_2024", "S1701", "Poverty, Poor, FPL, Poverty Rate"),
)

# 7. Insert one fake fact (6 values: area_id, metric_id, value, moe, source_id, status)
connection.execute(
    "INSERT INTO facts VALUES (?, ?, ?, ?, ?, ?)",
    ("house_45", "poverty_rate", 15.2, 2.1, "acs5_2024", "ok"),
)

# 8. Save everything
connection.commit()

# 9. Read it back and print each row
# 9. Read it back and print each row
print(pd.read_sql_query("SELECT * FROM sources", connection))
print(pd.read_sql_query("SELECT * FROM metrics", connection))
print(pd.read_sql_query("SELECT * FROM facts", connection))
connection.close()