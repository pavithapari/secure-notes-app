import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)''')
    conn.commit()
    conn.close()

# Call init_db to create the database and table when the app starts
init_db()

@app.route('/')
def home():
    # Fetch all notes from the database
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/add_note', methods=['POST'])
def add_note():
    if request.method == 'POST':
        note_title = request.form['title']
        note_content = request.form['content']

        # Insert the new note into the database
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()
        c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (note_title, note_content))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))

@app.route('/note/<int:note_id>')
def view_note(note_id):
    # Fetch a single note by its ID
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    note = c.fetchone()
    conn.close()

    return render_template('note.html', note=note)

if __name__ == '__main__':
    app.run(debug=True)
