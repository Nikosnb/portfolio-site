from flask import Flask, request, redirect, render_template, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"  # 🔐 важно за login

# 📌 Връзка с база
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# 📌 Създаване на база
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

# 📩 Изпращане
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

# 🔐 LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "1234":
            session['logged_in'] = True
            return redirect('/admin')
        else:
            return "Грешно потребителско име или парола"

    return render_template('login.html')

# 🚪 LOGOUT
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')

# 📊 ADMIN (защитен)
@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM messages ORDER BY id DESC")
    data = cursor.fetchall()

    conn.close()

    return render_template('admin.html', messages=data)

# 🚀 Стартиране
if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)