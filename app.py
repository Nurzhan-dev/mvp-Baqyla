from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from datetime import date
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'secret-key'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Простейшие пароли по ролям
CREDENTIALS = {
    "руководитель": "admin123",
    "сотрудник": "user123"
}

tasks = []

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        name = request.form.get("name")
        role = request.form.get("role")
        password = request.form.get("password")

        if CREDENTIALS.get(role) == password:
            session['name'] = name
            session['role'] = role
            return redirect(url_for("index"))
        else:
            error = "Неверный пароль"

    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/dashboard")
def dashboard():
    name = session.get("name", "Пользователь")
    return f"<h2>Добро пожаловать, {name}!</h2>"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/index', methods=['GET', 'POST'])
@app.route('/tasks', methods=['GET', 'POST'])
def index():
    if 'role' not in session or 'name' not in session:
        return redirect(url_for('login'))

    role = session['role']
    name = session['name']

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

    return render_template('index.html', tasks=tasks, role=role, name=name)

if __name__ == '__main__':
    app.run(debug=True)
