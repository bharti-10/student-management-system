import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="student_db"
)

cursor = conn.cursor()

# ➕ Add Student
def add_student():
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    course = input("Enter course: ")

    query = "INSERT INTO students (name, age, course) VALUES (%s, %s, %s)"
    values = (name, age, course)

    cursor.execute(query, values)
    conn.commit()

    print("✅ Student added successfully!")

# 📄 View Students
def view_students():
    cursor.execute("SELECT * FROM students")
    results = cursor.fetchall()

    print("\n--- Student Records ---")
    for row in results:
        print(row)
        
def update_student():
    student_id = int(input("Enter student ID to update: "))
    new_name = input("Enter new name: ")

    query = "UPDATE students SET name=%s WHERE id=%s"
    cursor.execute(query, (new_name, student_id))
    conn.commit()

    print("✅ Student updated successfully!")
def delete_student():
    student_id = int(input("Enter student ID to delete: "))

    query = "DELETE FROM students WHERE id=%s"
    cursor.execute(query, (student_id,))
    conn.commit()

    print("❌ Student deleted successfully!")

# 🎮 Menu system

while True:
    print("\n1. Add Student")
    print("2. View Students")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == '1':
        add_student()
    elif choice == '2':
        view_students()
    elif choice == '3':
        update_student()
    elif choice == '4':
        delete_student()
    elif choice == '5':
        print("Exiting...")
        break
    else:
        print("Invalid choice")