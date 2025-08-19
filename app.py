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
                short_url VARCHAR(6) UNIQUE,
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
        while is_short_url(short_url):  # Fixed: use function instead of checking against DATABASE string
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
                result = _getAllLink()
                return render_template('index.html', links=result)
        except sqlite3.Error as error:
            print(f"Database error: {error}")
            return render_template('index.html', error="Failed to create short URL")

    try:
        result = _getAllLink()
        return render_template('index.html', links=result)
    except sqlite3.Error as error:
        print(f"Database error: {error}")


def _getAllLink():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM urls ORDER BY created_at DESC")
        result = cur.fetchall()
        if len(result) == 0:
            return []

    return result




@app.route("/api/<int:id>", methods=['GET', 'POST','PUT'])
def update(id):
    if request.method in ['POST','PUT']:
        # Get form data correctly (should be parentheses, not brackets)
        new_short_url = request.form.get('short_url')
        new_long_url = request.form.get('long_url')

        if not new_short_url or not new_long_url:
            return render_template('404.html', error="Both short_url and long_url are required")

        try:
            with get_db() as conn:
                cur = conn.cursor()

                # Update the record where short_url matches the URL parameter
                cur.execute(
                    'UPDATE urls SET short_url = ?, long_url = ? WHERE id = ?',
                    (new_short_url, new_long_url, id)
                )

                if cur.rowcount == 0:
                    return render_template('404.html')

                conn.commit()

                cur.execute("SELECT * FROM urls WHERE id = ?", (id,))
                result = cur.fetchone()
                if result is None:
                    return render_template('404.html')
                return render_template('update.html', link=result)

        except sqlite3.Error as error:
            print(f"Database error: {error}")
            return render_template('update.html', error="Failed to update short URL")

    # GET request - return the form
    try:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM urls WHERE id = ?", (id,))
            result = cur.fetchone()
            if result is None:
                return render_template('404.html')

        return render_template('update.html', link=result)
    except sqlite3.Error as error:
        return render_template('404.html')

@app.route("/api/del/<int:id>", methods=['GET','POST','DELETE'])
def delete(id):
    if request.method == ['POST','DELETE']:
        short_url = request.form.get('short_url')
        long_url = request.form.get('long_url')

        if not short_url or not long_url:
            return render_template('404.html', error="Both short_url and long_url are required")

    try:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM urls WHERE id = ?", (id,))

            if cur.rowcount == 0:
                return render_template('success_delete.html')

            conn.commit()

            cur.execute("SELECT * FROM urls WHERE id = ?", (id,))
            result = cur.fetchone()
            if result is None:
                return render_template('404.html')
            return render_template('delete.html', error="Failed to delete short URL"
                                   )
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return render_template('delete.html', error="Failed to delete short URL")

    # try:
    #     with get_db() as conn:
    #         cur = conn.cursor()
    #         cur.execute("SELECT * FROM urls WHERE id = ?", (id,))
    #         result = cur.fetchone()
    #         if result is None:
    #             return render_template('404.html')
    #
    #     return render_template('delete.html', link=result)
    # except sqlite3.Error as error:
    #     return render_template('404.html')

@app.route("/l/<short_url>")
def redirect_short(short_url):
    try:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute('SELECT long_url FROM urls WHERE short_url = ?', (short_url,))
            result = cur.fetchone()
            cur.close()

            if result:
                long_url = result['long_url']
                return redirect(long_url, code=302)
            else:
                return "URL NOT FOUND", 404
    except sqlite3.Error:
        return "Database error", 500

if __name__ == "__main__":
    init_db()
    app.run(debug=True)