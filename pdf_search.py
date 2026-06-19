import sqlite3

def search_pdf(question):

    conn = sqlite3.connect('college.db')
    cursor = conn.cursor()

    cursor.execute("SELECT content FROM pdf_data")
    records = cursor.fetchall()

    conn.close()

    question = question.lower()

    for row in records:

        text = row[0]
        text_lower = text.lower()

        # Exact match
        if question in text_lower:
            return text[:2000]

        # Word-by-word match
        words = question.split()

        for word in words:
            if len(word) > 3 and word in text_lower:
                return text[:2000]

    return None