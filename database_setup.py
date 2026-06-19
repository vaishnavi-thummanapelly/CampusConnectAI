import sqlite3

conn = sqlite3.connect('college.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS college_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    details TEXT
)
''')

cursor.execute("""
INSERT INTO college_info (category, details)
VALUES
('fees', 'The annual fee is ₹85,000'),
('admission', 'Admissions start in June'),
('courses', 'CSE, ECE, IT, Mechanical, Civil Engineering'),
('placement', 'Top recruiters include TCS, Infosys, Wipro and Accenture')
""")

conn.commit()
conn.close()

print("Database Created Successfully!")