import sqlite3

def get_answer(question):

    conn = sqlite3.connect('college.db')

    cursor = conn.cursor()

    cursor.execute(
        "SELECT details FROM college_info WHERE category=?",
        (question,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return "Information not available."


def get_all_info():

    conn = sqlite3.connect('college.db')

    cursor = conn.cursor()

    cursor.execute(
        "SELECT category, details FROM college_info"
    )

    records = cursor.fetchall()

    conn.close()

    info = ""

    for row in records:
        info += f"{row[0]}: {row[1]}\n"

    return info