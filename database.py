import sqlite3
from flask import g

DATABASE = 'users.db'

def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # This allows accessing columns by name
    return g.db

def close_db(e=None):
    """Closes the database again at the end of the request."""
    db = g.pop('db', None)
    # Correct way to check if the database connection exists
    if db is not None:
        db.close()

def init_app(app):
    """Register database functions with the Flask app."""
    app.teardown_appcontext(close_db)

# --- User Functions ---

def get_all_users():
    db = get_db()
    return db.execute('SELECT id, name, email FROM users').fetchall()

def get_user_by_id(user_id):
    db = get_db()
    return db.execute('SELECT id, name, email FROM users WHERE id = ?', (user_id,)).fetchone()

def get_user_by_email(email):
    db = get_db()
    return db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

def create_user(name, email, hashed_password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
        (name, email, hashed_password)
    )
    db.commit()
    return cursor.lastrowid

def update_user(user_id, name, email):
    db = get_db()
    db.execute(
        'UPDATE users SET name = ?, email = ? WHERE id = ?',
        (name, email, user_id)
    )
    db.commit()

def delete_user(user_id):
    db = get_db()
    db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    db.commit()

def search_users_by_name(name):
    db = get_db()
    return db.execute('SELECT id, name, email FROM users WHERE name LIKE ?', ('%' + name + '%',)).fetchall()