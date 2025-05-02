from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3



app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()

    # Create table with time column
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''INSERT INTO notes(title, content) VALUES (?, ?)''', ('hello', 'sjoebgfue 081njqeotkhu'))
    conn.commit()
    conn.close()

# Call init_db at app start
init_db()

@app.route('/')
def home():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT id, title, CASE WHEN INSTR(content, CHAR(10)) > 0 THEN SUBSTR(content, 1, INSTR(content, CHAR(10)) - 1) ELSE content END AS first_line, time FROM notes ORDER BY id DESC LIMIT 8;")
    notes = [{"id": note[0], "title": note[1], "content": note[2], "timestamp": note[3]} for note in c.fetchall()]
    
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/note')
def allnotes():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    note = c.fetchall()
    conn.close()

    if note:
        return render_template('viewnotes.html', notes=note)
    else:
        return "Note not found", 404

@app.route('/note/<int:note_id>')
def view_note(note_id):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    
    # Fetch the note by its ID
    c.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    note = c.fetchone()
    conn.close()

    if note:
        # Pass the note as a dictionary to the template
        return render_template('note.html', notes={"id": note[0], "title": note[1], "content": note[2]})
    else:
        return "Note not found", 404
@app.route('/edit/<int:note_id>', methods=['POST'])
def edit_note(note_id):
    title = request.form['title']
    content = request.form['content']
    
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    (c.execute("UPDATE notes SET title=?, content=? WHERE id=?", (title, content, note_id)))
    

    conn.commit()
    conn.close()
    
    return redirect(url_for('home'))
@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('home'))
@app.route('/delete_all', methods=['POST'])
def delete_all():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("DELETE FROM notes")  
    conn.commit()
    conn.close()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
