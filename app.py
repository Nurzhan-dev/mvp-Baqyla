
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from datetime import date
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'secret-key'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

tasks = []

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        session['role'] = role
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'role' not in session:
        return redirect(url_for('login'))

    role = session['role']

    if request.method == 'POST' and role == 'руководитель':
        file = request.files['document']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        tasks.append({
            'title': request.form['title'],
            'responsible': request.form['responsible'],
            'due_date': request.form['due_date'],
            'document': filename
        })

        return redirect(url_for('index'))

    today = date.today().isoformat()
    for task in tasks:
        task['status'] = (
            'Просрочено' if task['due_date'] < today else
            'Срочно' if task['due_date'] == today else
            'Новое'
        )
    return render_template('index.html', tasks=tasks, role=role)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run()