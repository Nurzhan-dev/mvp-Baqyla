from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug.utils import secure_filename
from datetime import date
import os

app = Flask(__name__)
app.secret_key = "secret-key"
app.config["UPLOAD_FOLDER"] = "uploads"

CREDENTIALS = {
    "руководитель": "admin123",
    "сотрудник": "user123"
}

tasks = []

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        name = request.form["name"]
        role = request.form["role"]
        password = request.form["password"]
        if CREDENTIALS.get(role) == password:
            session["name"] = name
            session["role"] = role
            return redirect(url_for("index"))
        else:
            error = "Неверный пароль"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/index", methods=["GET", "POST"])
def index():
    if "role" not in session:
        return redirect(url_for("login"))

    role = session["role"]
    name = session.get("name", "Пользователь")

    if request.method == "POST" and role == "руководитель":
        file = request.files["document"]
        filename = secure_filename(file.filename)
        if filename:
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        else:
            filename = None
        tasks.append({
            "title": request.form["title"],
            "responsible": request.form["responsible"],
            "due_date": request.form["due_date"],
            "document": filename
        })
        return redirect(url_for("index"))

    today = date.today().isoformat()
    for task in tasks:
        task["status"] = (
            "Просрочено" if task["due_date"] < today else
            "Срочно" if task["due_date"] == today else
            "Новое"
        )
    return render_template("index.html", tasks=tasks, role=role, name=name)
