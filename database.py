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
    except sqlite3.Error as e:
        print(f"Database error while creating table: {e}")
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
    except sqlite3.Error as e:
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
    except sqlite3.Error as e:
        print(f"Database error while fetching: {e}")
        return []
    finally:
        conn.close()

def search_student(roll_number):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, course, marks FROM students WHERE roll_no = ?", (roll_number,))
        row = cursor.fetchone()
        return row
    except sqlite3.Error as e:
        print(f"Database error while searching: {e}")
        return None
    finally:
        conn.close()

def update_student(old_roll_number, name, course, marks, new_roll_number=None):
    """
    Update student. Supports changing roll number with duplicate check.
    If new_roll_number is None or same as old, roll_no is not changed.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # If roll number is being changed, check for duplicate
        if new_roll_number is not None and new_roll_number != old_roll_number:
            cursor.execute("SELECT 1 FROM students WHERE roll_no = ?", (new_roll_number,))
            if cursor.fetchone():
                return False, f"Error: Roll Number {new_roll_number} already assigned to another student!"

        # Use new roll if provided, else keep old
        final_roll = new_roll_number if new_roll_number is not None else old_roll_number

        cursor.execute("UPDATE students SET roll_no = ?, name = ?, course = ?, marks = ? WHERE roll_no = ?",
                       (final_roll, name, course, marks, old_roll_number))
        conn.commit()
        if cursor.rowcount == 0:
            return False, f"Student with Roll Number {old_roll_number} not found!"
        return True, "Student record updated successfully!"
    except sqlite3.Error as e:
        return False, f"Database Error: {e}"
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
    except sqlite3.Error as e:
        return False, f"Database Error: {e}"
    finally:
        conn.close()