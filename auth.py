# auth.py
import uuid
import sqlite3
from utils import get_db
import bcrypt
import streamlit as st


def create_user(username, password):
    conn = get_db()
    cursor = conn.cursor()
    try:
        user_id = str(uuid.uuid4())
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cursor.execute("INSERT INTO users (id, username, password_hash) VALUES (?, ?, ?)", (user_id, username, hashed_pw))
        conn.commit()
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row and bcrypt.checkpw(password.encode(), row[1].encode()):
        return row[0]
    return None

def delete_user(user_id):
    conn = get_db()
    cursor = conn.cursor()

    # First delete related records from child tables
    cursor.execute("DELETE FROM chats WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM timetables WHERE user_id = ?", (user_id,))

    # Now it's safe to delete the user
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))

    conn.commit()
    conn.close()


def logout():
    for key in ["user_id", "username", "is_guest"]:
        st.session_state.pop(key, None)
