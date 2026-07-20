import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# ==========================
# PORTFOLIO TABLE
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS portfolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    file_name TEXT,
    file_type TEXT DEFAULT 'image',
    youtube_url TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ==========================
# ADMIN TABLE
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT NOT NULL
)
""")

# ==========================
# SAFE MIGRATION
# ==========================

try:
    cursor.execute("ALTER TABLE portfolio ADD COLUMN file_type TEXT DEFAULT 'image'")
except:
    pass

try:
    cursor.execute("ALTER TABLE portfolio ADD COLUMN youtube_url TEXT")
except:
    pass

try:
    cursor.execute("ALTER TABLE portfolio ADD COLUMN description TEXT")
except:
    pass

try:
    cursor.execute("ALTER TABLE portfolio ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
except:
    pass

conn.commit()
conn.close()

print("✅ Database ready!")