from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize db
def init_db():
    conn = get_db_connection()
    conn.execute('''
                 CREATE TABLE IF NOT EXISTS tasks (
                 id INTEGER PRIMARY KEY, 
                 title TEXT NOT NULL, 
                 done BOOLEAN NOT NULL,
                 created_at TEXT,
                 due_date TEXT,
                 completed_at TEXT
                 )
            ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    due_date = request.form['due_date']
    conn = get_db_connection()
    conn.execute("INSERT INTO tasks (title, done, created_at, due_date) VALUES (?, ?, ?, ?)", 
                 (title, False, datetime.now().isoformat(), due_date))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    conn = get_db_connection()
    conn.execute("UPDATE tasks SET done = 1, completed_at = ? WHERE id = ?", 
                 (datetime.now().isoformat(), task_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
