from datetime import datetime, timedelta
import sqlite3
from contextlib import contextmanager
from typing import List, Optional
from models import UrlRepository, Url, AuthRepository


class SQLiteUrlRepository(UrlRepository):
    def __init__(self, database_path: str):
        self.database_path = database_path
        self._init_db()

    def _init_db(self):
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute('''
                        CREATE TABLE IF NOT EXISTS urls (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            short_url VARCHAR(6) UNIQUE NOT NULL,
                            long_url TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    ''')
                conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Error connecting to database: {e}")

    @contextmanager
    def _get_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.database_path)
            conn.row_factory = sqlite3.Row
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Database error: {e}")
        finally:
            if conn:
                conn.close()

    def save(self, url: Url) -> Url:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                    'INSERT INTO urls (short_url, long_url) VALUES (?, ?)',
                    (url.short_url, url.long_url)
                )
            conn.commit()
            url.id = cur.lastrowid
            return url

    def find_by_short_url(self, short_url: str) -> Optional[Url]:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM urls WHERE short_url = ?', (short_url,))
            row = cur.fetchone()
            return self._row_to_url(row) if row else None

    def find_by_id(self, url_id: int) -> Optional[Url]:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM urls WHERE id = ?', (url_id,))
            row = cur.fetchone()
            return self._row_to_url(row) if row else None

    def get_all(self) -> List[Url]:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM urls')
            rows = cur.fetchall()
            return [self._row_to_url(row) for row in rows]

    def update(self, url_id: int, short_url: str, long_url: str) -> Optional[Url]:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                    'UPDATE urls SET short_url = ?, long_url = ? WHERE id = ?',
                    (short_url, long_url, url_id)
                )
            if cur.rowcount == 0:
                return None
            conn.commit()
            return self.find_by_id(url_id)

    def delete(self, url_id: int) -> bool:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute('DELETE FROM urls WHERE id = ?', (url_id,))
            deleted = cur.rowcount = 0
            conn.commit()
            return deleted

    def exists_by_short_url(self, short_url: str) -> bool:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute('SELECT 1 FROM urls WHERE short_url = ?', (short_url,))
            return cur.fetchone() is not None

    def _row_to_url(self, row) -> Url:
        return Url(
            id=row['id'],
            short_url=row['short_url'],
            long_url=row['long_url'],
            created_at=datetime.fromisoformat(row['created_at'])
        )


class InMemoryAuthRepository(AuthRepository):
    def __init__(self):
        self.users = {'admin': '123456'}

    def validate_user(self, username: str, password:str) -> bool:
        return self.users.get(username) == password