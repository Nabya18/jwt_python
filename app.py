from flask import Flask, render_template, request, redirect
import string
import random
import sqlite3
from contextlib import contextmanager

app = Flask(__name__)

DATABASE = 'urls.db'

def init_db():
    try:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_url TEXT UNIQUE,
                long_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
                    ''')
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully")
    except sqlite3.Error as error:
        print(f"Error while connecting to database: {error}")
        raise

@contextmanager
def get_db():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as error:
        if conn:
            conn.rollback()
        print(f"Database error: {error}")
        raise
    finally:
        if conn:
            conn.close()


def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(chars) for _ in range(length))
    return short_url

def is_short_url(short_url):
    try:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute('SELECT 1 FROM urls WHERE short_url = ?', (short_url,))
            result = cur.fetchone() is not None
            cur.close()
            return result
    except sqlite3.Error as error:
        print(error)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']

        short_url = generate_short_url()
        while short_url in DATABASE:
            short_url = generate_short_url()
        try:
            with get_db() as conn:
                cur = conn.cursor()
                cur.execute(
                    'INSERT INTO urls (short_url, long_url) VALUES (?, ?)',
                    (short_url, long_url)
                )
                conn.commit()
                cur.close()
                return render_template('index.html', short_url=short_url, long_url=long_url)
        except sqlite3.Error as error:
            print(f"Database error: {error}")
            return render_template('index.html', error="Failed to create short URL")

    return render_template('index.html')


@app.route("/api/v1/<short_url>")
def redirect_short(short_url):
    try:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute('SELECT long_url FROM urls WHERE short_url = ?', (short_url,))
            result = cur.fetchone()
            cur.close()

            if result:
                long_url = result['long_url']
                return redirect(long_url)
            else:
                return "URL NOT FOUND", 404
    except sqlite3.Error:
        return "Database error", 500

if __name__ == "__main__":
    init_db()
    app.run(debug=True)