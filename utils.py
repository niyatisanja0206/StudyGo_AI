#utils.py
import streamlit as st
import sqlite3
import json
import os

# ---------------- CSS Loader ----------------
def load_css(file_path="theme.css"):
    if os.path.exists(file_path):
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ---------------- SQLite Database Setup ----------------
DB_PATH = "database.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = 1")
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE,
        password_hash TEXT
    )
    """)

    # Chats
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        title TEXT,
        messages_json TEXT,
        timestamp TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # Timetables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS timetables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        name TEXT,
        schedule_json TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)


    conn.commit()
    conn.close()

init_db()

# ---------------- DB Helper Functions ----------------
def save_chat(user_id, title, messages, timestamp):
    conn = get_db()
    cursor = conn.cursor()
    messages_json = json.dumps(messages)
    cursor.execute("""
        INSERT INTO chats (user_id, title, messages_json, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_id, title, messages_json, timestamp))
    conn.commit()
    conn.close()

def load_chats(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT title, messages_json, timestamp FROM chats WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "title": row[0],
            "messages": json.loads(row[1]),
            "timestamp": row[2]
        }
        for row in rows
    ]

def delete_chat(user_id, title):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chats WHERE user_id = ? AND title = ?", (user_id, title))
    conn.commit()
    conn.close()

def save_timetable(user_id, name, schedule):
    conn = get_db()
    cursor = conn.cursor()
    schedule_json = json.dumps(schedule)
    cursor.execute("""
        INSERT OR REPLACE INTO timetables (user_id, name, schedule_json)
        VALUES (?, ?, ?)
    """, (user_id, name, schedule_json))
    conn.commit()
    conn.close()

def load_timetables(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, schedule_json FROM timetables WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return {
        row[0]: json.loads(row[1]) for row in rows
    }
