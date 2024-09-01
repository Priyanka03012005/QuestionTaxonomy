from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = "question"

# Database configuration
DATABASE = 'database.db'

def get_db():
    if 'db' not in g:
        g.db = sql.connect(DATABASE)
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Create tables if not exist
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Question (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT NOT NULL,
                taxonomy_level TEXT NOT NULL,
                topic TEXT NOT NULL
            )
        ''')
        db.commit()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create_question():
    if request.method == 'POST':
        question_text = request.form['question_text']
        taxonomy_level = request.form['taxonomy_level']
        topic = request.form['topic']
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO Question (question_text, taxonomy_level, topic)
            VALUES (?, ?, ?)
        ''', (question_text, taxonomy_level, topic))
        db.commit()
        
        return redirect(url_for('view_questions'))
    return render_template('create_question.html')

@app.route('/questions')
def view_questions():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT question_text, taxonomy_level, topic FROM Question')
    questions = cursor.fetchall()
    return render_template('view_questions.html', questions=questions)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
