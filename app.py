from flask import Flask, render_template, request, redirect, url_for, session, g, flash
import sqlite3 as sql
from werkzeug.security import generate_password_hash, check_password_hash

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
            CREATE TABLE IF NOT EXISTS User (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS SearchHistory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                search_term TEXT NOT NULL,
                taxonomy_level TEXT NOT NULL,
                search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES User(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Question (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT NOT NULL,
                taxonomy_level TEXT NOT NULL,
                topic TEXT NOT NULL
            )
        ''')
        
        db.commit()

# User authentication
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']
        
        db = get_db()
        cursor = db.cursor()
        
        try:
            cursor.execute('INSERT INTO User (username, password, role) VALUES (?, ?, ?)', (username, password, role))
            db.commit()
            flash('Signup successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sql.IntegrityError:
            flash('Username already exists!', 'error')
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM User WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

# Admin route to create questions
@app.route('/admin/create', methods=['GET', 'POST'])
def create_question():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        question_text = request.form['question_text']
        taxonomy_level = request.form['taxonomy_level']
        topic = request.form['topic']
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO Question (question_text, taxonomy_level, topic) VALUES (?, ?, ?)', (question_text, taxonomy_level, topic))
        db.commit()
        
        flash('Question created successfully!', 'success')
        return redirect(url_for('view_questions'))
    
    return render_template('create_question.html')

@app.route('/admin/questions')
def view_questions():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT question_text, taxonomy_level, topic FROM Question')
    questions = cursor.fetchall()
    return render_template('view_questions.html', questions=questions)

# User route to search for questions
@app.route('/user', methods=['GET', 'POST'])
def user_interface():
    if 'user_id' not in session or session.get('role') != 'user':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        random_question = request.form['random_question']
        taxonomy_level = request.form['taxonomy_level']
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT question_text FROM Question WHERE taxonomy_level = ? AND question_text LIKE ?', (taxonomy_level, f'%{random_question}%'))
        questions = cursor.fetchall()
        
        # Track the search activity
        cursor.execute('INSERT INTO SearchHistory (user_id, search_term, taxonomy_level) VALUES (?, ?, ?)', (session['user_id'], random_question, taxonomy_level))
        db.commit()
        
        return render_template('user_view.html', questions=questions, random_question=random_question)
    
    return render_template('user_interface.html')

# User route to view search history
@app.route('/user/history')
def user_history():
    if 'user_id' not in session or session.get('role') != 'user':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT search_term, taxonomy_level, search_time FROM SearchHistory WHERE user_id = ? ORDER BY search_time DESC', (session['user_id'],))
    history = cursor.fetchall()
    return render_template('user_history.html', history=history)

@app.route('/')
def index():
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('create_question'))
        elif session.get('role') == 'user':
            return redirect(url_for('user_interface'))
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)