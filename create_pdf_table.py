import sqlite3

conn = sqlite3.connect('college.db')

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pdf_data(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    content TEXT
)
""")

conn.commit()
conn.close()

print("PDF table created successfully!")