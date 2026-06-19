from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
from PyPDF2 import PdfReader
from pdf_search import search_pdf
from gemini_chat import ask_gemini

if not os.path.exists("uploads"):
    os.makedirs("uploads")

app = Flask(__name__)
app.secret_key = "campusconnect_secret_key"

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():

    response = ""

    if request.method == 'POST':

       question = request.form['question']

       pdf_answer = search_pdf(question)

       if pdf_answer:
            response = pdf_answer
       else:
            response = ask_gemini(question)
    return render_template('chatbot.html', response=response)
@app.route('/login', methods=['GET', 'POST'])
def login():

    error = ""

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":

            session['admin'] = True

            return redirect(url_for('admin'))

        else:
            error = "Invalid Username or Password"

    return render_template('login.html', error=error)
@app.route('/logout')
def logout():

    session.pop('admin', None)

    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('college.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        category = request.form['category']
        details = request.form['details']

        cursor.execute(
            "INSERT INTO college_info(category, details) VALUES (?, ?)",
            (category, details)
        )

        conn.commit()

    cursor.execute("SELECT * FROM college_info")
    records = cursor.fetchall()

    conn.close()

    return render_template('admin.html', records=records)
@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect('college.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM college_info WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('admin'))
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    conn = sqlite3.connect('college.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        category = request.form['category']
        details = request.form['details']

        cursor.execute(
            "UPDATE college_info SET category=?, details=? WHERE id=?",
            (category, details, id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('admin'))

    cursor.execute(
        "SELECT * FROM college_info WHERE id=?",
        (id,)
    )

    record = cursor.fetchone()

    conn.close()

    return render_template('edit.html', record=record)
@app.route('/upload_pdf', methods=['GET', 'POST'])
def upload_pdf():

    text = ""

    if request.method == 'POST':

        file = request.files['pdf']

        if file:

            filepath = os.path.join("uploads", file.filename)
            file.save(filepath)

            reader = PdfReader(filepath)

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text

            conn = sqlite3.connect('college.db')
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO pdf_data(filename, content)
                VALUES (?, ?)
                """,
                (file.filename, text)
            )

            conn.commit()
            conn.close()

            return f"""
            <h2>PDF Uploaded and Saved Successfully</h2>
            <h3>File:</h3>
            <p>{file.filename}</p>
            <hr>
            <pre>{text[:3000]}</pre>
            """

    return render_template('upload_pdf.html')

if __name__ == '__main__':
    app.run(debug=True)