# main.py - Menu driven Student Record Management System
import math
from student import Student
import database

def add_student():
    """Add a new student with all validations."""
    print("\n--- Add Student ---")
    try:
        roll_input = input("Enter Roll Number: ").strip()
        roll_number = int(roll_input)
        if roll_number <= 0:
            print("Error: Roll number must be a positive integer!")
            return
    except ValueError:
        print("Error: Roll number must be a number!")
        return

    name = input("Enter Name: ").strip()
    if not name:
        print("Error: Name cannot be empty!")
        return

    course = input("Enter Course: ").strip()
    if not course:
        print("Error: Course cannot be empty!")
        return

    try:
        marks = float(input("Enter Marks (0-100): ").strip())
        if not math.isfinite(marks) or marks < 0 or marks > 100:
            print("Error: Marks must be between 0 and 100!")
            return
    except ValueError:
        print("Error: Marks must be a number!")
        return

    student = Student(roll_number, name, course, marks)
    success, message = database.add_student(student)
    print(message)


def view_all_students():
    """Display all student records."""
    print("\n--- View All Students ---")
    rows = database.get_all_students()
    if not rows:
        print("No student records found!")
        return

    print(f"Total Students: {len(rows)}\n")
    for row in rows:
        student = Student(row[0], row[1], row[2], row[3])
        student.display()


def search_student():
    """Search student by roll number."""
    print("\n--- Search Student ---")
    try:
        roll_number = int(input("Enter Roll Number to Search: ").strip())
    except ValueError:
        print("Error: Please enter a valid numeric roll number!")
        return

    row = database.search_student(roll_number)
    if row:
        print("Student Found:\n")
        student = Student(row[0], row[1], row[2], row[3])
        student.display()
    else:
        print(f"Student with Roll Number {roll_number} not found!")


def update_student():
    """Update student details by roll number."""
    print("\n--- Update Student ---")
    try:
        roll_number = int(input("Enter Roll Number to Update: ").strip())
    except ValueError:
        print("Error: Please enter a valid numeric roll number!")
        return

    row = database.search_student(roll_number)
    if row is None:
        print(f"Student with Roll Number {roll_number} not found!")
        return

    found_student = Student(row[0], row[1], row[2], row[3])
    print("Found student. Leave blank and press Enter to keep existing value.\n")
    found_student.display()

    new_name = input(f"Enter New Name [{found_student.name}]: ").strip()
    if new_name:
        found_student.name = new_name

    new_course = input(f"Enter New Course [{found_student.course}]: ").strip()
    if new_course:
        found_student.course = new_course

    new_marks_input = input(f"Enter New Marks [{found_student.marks}]: ").strip()
    if new_marks_input:
        try:
            new_marks = float(new_marks_input)
            if not math.isfinite(new_marks) or new_marks < 0 or new_marks > 100:
                print("Error: Marks must be between 0 and 100! Marks not updated.")
            else:
                found_student.marks = new_marks
        except ValueError:
            print("Error: Invalid marks! Marks not updated.")

    success, message = database.update_student(found_student.roll_number, found_student.name, found_student.course, found_student.marks)
    print(message)


def delete_student():
    """Delete student by roll number after confirmation."""
    print("\n--- Delete Student ---")
    try:
        roll_number = int(input("Enter Roll Number to Delete: ").strip())
    except ValueError:
        print("Error: Please enter a valid numeric roll number!")
        return

    row = database.search_student(roll_number)
    if row is None:
        print(f"Student with Roll Number {roll_number} not found!")
        return
    
    student = Student(row[0], row[1], row[2], row[3])
    print("Student Found:\n")
    student.display()
    confirm = input(f"Are you sure you want to delete Roll No {roll_number}? (y/n): ").strip().lower()
    if confirm in ("y", "yes"):
        success, message = database.delete_student(roll_number)
        print(message)
    else:
        print("Deletion cancelled.")


def main():
    """Main menu loop."""
    database.create_table()
    print("Database initialized successfully. (students.db ready)")
    
    while True:
        print("\n===== Student Record Management System =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_student()
        elif choice == "2":
            view_all_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("\nThank you for using Student Record Management System. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()