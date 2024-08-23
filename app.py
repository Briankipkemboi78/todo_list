from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


# Initialize db
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT, done BOOLEAN)')
    conn.close()

init_db()


@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (title, False))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    conn = sqlite3.connect('database.db')
    conn.execute("UPDATE tasks SET done = ? WHERE id = ?", (True, task_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect('database.db')
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True)