from flask import Flask, request, redirect, render_template
import sqlite3
import os

app = Flask(__name__)

# 📌 Функция за база
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# 📌 Създаване на база ако я няма
def init_db():
    if not os.path.exists('database.db'):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                message TEXT
            )
        ''')

        conn.commit()
        conn.close()

# 🏠 Начална страница
@app.route('/')
def home():
    return render_template('index.html')

# 📩 Изпращане на съобщение
@app.route('/send', methods=['POST'])
def send():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
        (name, email, message)
    )

    conn.commit()
    conn.close()

    return redirect('/')

# 📊 ADMIN DASHBOARD
@app.route('/admin')
def admin():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM messages ORDER BY id DESC")
    data = cursor.fetchall()

    conn.close()

    return render_template('admin.html', messages=data)

# 🚀 Стартиране
if __name__ == "__main__":
    init_db()
    app.run(debug=True)