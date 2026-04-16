from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)

# 📌 Създаване на база данни
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
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

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
        (name, email, message)
    )

    conn.commit()
    conn.close()

    return redirect('/')

# 📊 ADMIN DASHBOARD (модерен)
@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM messages ORDER BY id DESC")
    data = cursor.fetchall()

    conn.close()

    return render_template('admin.html', messages=data)

# ▶️ Стартиране
if __name__ == '__main__':
    init_db()
    app.run(debug=True)