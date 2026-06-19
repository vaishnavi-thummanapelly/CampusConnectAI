import sqlite3

conn = sqlite3.connect('college.db')

cursor = conn.cursor()

cursor.execute("SELECT * FROM pdf_data")

records = cursor.fetchall()

for row in records:
    print(row)

conn.close()