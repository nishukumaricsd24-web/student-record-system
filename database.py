# database.py - Handle database connection and operations
import sqlite3

DB_NAME = "students.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    """Create students table if not exists"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                roll_no INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                course TEXT NOT NULL,
                marks REAL NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()

def add_student(student):
    """Insert student. Handles duplicate roll_no."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # Parameterized query to prevent SQL injection
        cursor.execute("INSERT INTO students (roll_no, name, course, marks) VALUES (?, ?, ?, ?)",
                       (student.roll_number, student.name, student.course, student.marks))
        conn.commit()
        return True, "Student added successfully!"
    except sqlite3.IntegrityError:
        return False, f"Error: Student with Roll Number {student.roll_number} already exists!"
    except Exception as e:
        return False, f"Database Error: {e}"
    finally:
        conn.close()

def get_all_students():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, course, marks FROM students")
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

def search_student(roll_number):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, course, marks FROM students WHERE roll_no = ?", (roll_number,))
        row = cursor.fetchone()
        return row
    finally:
        conn.close()

def update_student(roll_number, name, course, marks):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, marks = ? WHERE roll_no = ?",
                       (name, course, marks, roll_number))
        conn.commit()
        if cursor.rowcount == 0:
            return False, f"Student with Roll Number {roll_number} not found!"
        return True, "Student record updated successfully!"
    finally:
        conn.close()

def delete_student(roll_number):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE roll_no = ?", (roll_number,))
        conn.commit()
        if cursor.rowcount == 0:
            return False, f"Student with Roll Number {roll_number} not found!"
        return True, "Student deleted successfully!"
    finally:
        conn.close()