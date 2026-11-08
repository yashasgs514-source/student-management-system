import os
import sqlite3
from pathlib import Path

from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-this-key")

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "students.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL,
            marks INTEGER NOT NULL CHECK (marks BETWEEN 0 AND 100)
        )
    """)
    connection.commit()
    connection.close()


@app.route("/")
def index():
    search = request.args.get("q", "").strip()
    connection = get_db_connection()

    if search:
        students = connection.execute(
            """SELECT * FROM students
               WHERE name LIKE ? OR email LIKE ? OR course LIKE ?
               ORDER BY id DESC""",
            (f"%{search}%", f"%{search}%", f"%{search}%")
        ).fetchall()
    else:
        students = connection.execute(
            "SELECT * FROM students ORDER BY id DESC"
        ).fetchall()

    connection.close()
    return render_template("index.html", students=students, search=search)


@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        course = request.form.get("course", "").strip()
        marks_text = request.form.get("marks", "").strip()

        if not name or not email or not course or not marks_text:
            flash("Please fill in every field.", "error")
            return render_template("student_form.html", student=None)

        try:
            marks = int(marks_text)
        except ValueError:
            flash("Marks must be a whole number.", "error")
            return render_template("student_form.html", student=None)

        if not 0 <= marks <= 100:
            flash("Marks must be between 0 and 100.", "error")
            return render_template("student_form.html", student=None)

        connection = get_db_connection()
        connection.execute(
            "INSERT INTO students (name, email, course, marks) VALUES (?, ?, ?, ?)",
            (name, email, course, marks)
        )
        connection.commit()
        connection.close()

        flash("Student added successfully.", "success")
        return redirect(url_for("index"))

    return render_template("student_form.html", student=None)


@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    connection = get_db_connection()
    student = connection.execute(
        "SELECT * FROM students WHERE id = ?", (student_id,)
    ).fetchone()

    if student is None:
        connection.close()
        abort(404)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        course = request.form.get("course", "").strip()
        marks_text = request.form.get("marks", "").strip()

        try:
            marks = int(marks_text)
        except ValueError:
            marks = -1

        if not name or not email or not course or not 0 <= marks <= 100:
            flash("Enter all fields and marks between 0 and 100.", "error")
            connection.close()
            return render_template("student_form.html", student={
                "id": student_id, "name": name, "email": email,
                "course": course, "marks": marks_text
            })

        connection.execute(
            """UPDATE students
               SET name = ?, email = ?, course = ?, marks = ?
               WHERE id = ?""",
            (name, email, course, marks, student_id)
        )
        connection.commit()
        connection.close()

        flash("Student updated successfully.", "success")
        return redirect(url_for("index"))

    connection.close()
    return render_template("student_form.html", student=student)


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    connection = get_db_connection()
    connection.execute("DELETE FROM students WHERE id = ?", (student_id,))
    connection.commit()
    connection.close()

    flash("Student deleted.", "success")
    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(debug=True)
