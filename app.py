import os
from urllib.parse import urlparse
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# ✅ Function to get fresh DB connection every time
def get_db():
    url = urlparse(os.getenv("DATABASE_URL"))
    
    conn = mysql.connector.connect(
        host=url.hostname,
        user=url.username,
        password=url.password,
        database=url.path[1:],   # remove '/'
        port=url.port
    )
    
    return conn


# ✅ Home route
@app.route('/')
def home():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    return render_template('index.html', students=students)


# ✅ Add student
@app.route('/add', methods=['POST'])
def add():
    conn = get_db()
    cursor = conn.cursor()

    name = request.form['name']
    age = int(request.form['age'])
    course = request.form['course']

    cursor.execute(
        "INSERT INTO students (name, age, course) VALUES (%s, %s, %s)",
        (name, age, course)
    )

    conn.commit()
    conn.close()

    return redirect('/')


# ✅ Edit page
@app.route('/edit/<int:id>')
def edit(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()

    conn.close()

    return render_template('edit.html', student=student)


# ✅ Update student
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    conn = get_db()
    cursor = conn.cursor()

    name = request.form['name']
    age = request.form['age']
    course = request.form['course']

    cursor.execute(
        "UPDATE students SET name=%s, age=%s, course=%s WHERE id=%s",
        (name, age, course, id)
    )

    conn.commit()
    conn.close()

    return redirect('/')


# ✅ Delete student
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    
    conn.commit()
    conn.close()

    return redirect('/')


# ✅ Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)