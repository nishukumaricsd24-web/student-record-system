# database.py - Handle database connection and operations
import sqlite3

DB_NAME = "students.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    """Create students table if not exists with new schema"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                roll_no INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                course TEXT NOT NULL,
                marks REAL NOT NULL,
                section TEXT,
                phone TEXT,
                email TEXT
            )
        """)
        conn.commit()
        migrate_database(conn) # ensure old DB is upgraded
    except sqlite3.Error as e:
        print(f"Database error while creating table: {e}")
    finally:
        conn.close()

def migrate_database(conn=None):
    """Add new columns if they don\'t exist - preserves existing records"""
    close_later = False
    if conn is None:
        conn = get_connection()
        close_later = True
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(students)")
        cols = [c[1] for c in cursor.fetchall()]
        if "section" not in cols:
            cursor.execute("ALTER TABLE students ADD COLUMN section TEXT")
        if "phone" not in cols:
            cursor.execute("ALTER TABLE students ADD COLUMN phone TEXT")
        if "email" not in cols:
            cursor.execute("ALTER TABLE students ADD COLUMN email TEXT")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Migration note: {e}")
    finally:
        if close_later:
            conn.close()

def add_student(student):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (roll_no, name, course, section, phone, marks, email) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (student.roll_number, student.name, student.course, student.section, student.phone, student.marks, student.email))
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
        cursor.execute("SELECT roll_no, name, course, section, phone, marks, email FROM students")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error while fetching: {e}")
        return []
    finally:
        conn.close()

def search_student(roll_number):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, course, section, phone, marks, email FROM students WHERE roll_no = ?", (roll_number,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Database error while searching: {e}")
        return None
    finally:
        conn.close()

def search_by_name(name_query):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, course, section, phone, marks, email FROM students WHERE name LIKE ?", (f"%{name_query}%",))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()

def update_student(old_roll_number, name, course, section, phone, marks, email, new_roll_number=None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if new_roll_number is not None and new_roll_number != old_roll_number:
            cursor.execute("SELECT 1 FROM students WHERE roll_no = ?", (new_roll_number,))
            if cursor.fetchone():
                return False, f"Error: Roll Number {new_roll_number} already assigned!"
        final_roll = new_roll_number if new_roll_number is not None else old_roll_number
        cursor.execute("UPDATE students SET roll_no=?, name=?, course=?, section=?, phone=?, marks=?, email=? WHERE roll_no=?",
                       (final_roll, name, course, section, phone, marks, email, old_roll_number))
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