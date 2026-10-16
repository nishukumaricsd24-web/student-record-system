# Student Record Management System

A professional desktop application built with Python, Tkinter and SQLite to manage student records efficiently. Available as both a modern Blue-White GUI and a CLI version sharing the same database.

## Features

### Core Functionality
- Add new student records
- View all students
- Search by Roll Number or Student Name
- Update student details (including Roll Number with duplicate check)
- Delete student records with confirmation
- Course-wise Student Records with Section filter
- Validations & duplicate prevention
- Persistent SQLite storage

### GUI Highlights (`gui.py`)
- Modern Blue-White dashboard with sidebar navigation
- **Initial Screen:** Only Student Registration form is visible on startup
- **Step-wise Registration Flow:**
  1. Select Course (Dropdown)
  2. Select Section (Dependent on Course - disabled until course is selected)
  3. Enter Student Details - Name, Roll Number, Phone Number, Marks
- Sidebar Navigation: `Add Student` | `View Students` | `Search Student` | `Student Records`
- Single-screen navigation - only one screen visible at a time
- `View Students` - Shows all students in a clean table
- `Search Student` - Separate search screen, results shown only after search
- `Student Records` - Course cards first -> Click course -> Only that course's students appear -> Section filter + Back to Courses button
- Single table layout (duplicate table issue fixed)
- Tkinter Treeview with alternating row colors, scrollbar and auto-refresh
- Confirmation dialogs and success/error popups
- Resizable, responsive and professional design

### Validation
- Course and Section are required
- Roll Number must be unique and numeric
- Student Name cannot be empty
- Phone Number must be exactly 10 digits
- Marks must be numeric between 0 and 100
- Helpful messages for invalid input

## Technologies Used
- Python 3
- SQLite (students.db)
- Tkinter (built-in, no extra dependencies)
- Git and GitHub
- Visual Studio Code

## Project Structure

student-record-system/
├── main.py # CLI version (unchanged)
├── student.py # Student class blueprint
├── database.py # SQLite operations (reused by CLI & GUI)
├── gui.py # Tkinter GUI - Blue-White Dashboard
├── students.db # Created automatically on first run
├── .gitignore
└── README.md
code

Copy

## Database
SQLite `students.db` with table:
sql
CREATE TABLE students (
roll_no INTEGER PRIMARY KEY,
name TEXT NOT NULL,
course TEXT NOT NULL,
marks REAL NOT NULL,
section TEXT,
phone TEXT,
email TEXT
);
code

Copy
Uses parameterized queries. Auto-created via `database.create_table()` and auto-migrated with `ALTER TABLE ADD COLUMN` to preserve existing records. No duplicate tables.

## How to Run

### Option 1: GUI (Recommended)
bash
python gui.py
code

Copy

### Option 2: CLI
bash
python main.py
code

Copy
Both share the same `students.db` - records are interchangeable.

## How to Use

| Navigation | Behaviour |
|---|---|
| **App Opens** | Shows only `Add Student` registration form |
| **Add Student** | Select Course -> Select Section -> Fill Name, Roll No, Phone, Marks -> Click `Add Student` |
| **View Students** | Click `View Students` -> All students displayed in table |
| **Search Student** | Click `Search Student` -> Enter Roll No or Name -> Click `Search` -> Matching results appear |
| **Student Records** | Click `Student Records` -> Course cards appear -> Click a course -> Only that course's students appear -> Use Section filter if needed -> Click `Back to Courses` to return |

To manage courses easily, edit top of `gui.py`:
python
COURSES = ["Diploma in Computer Science", "BCA", "B.Tech", "BBA", "MCA"]
COURSE_SECTIONS = {
"Diploma": ["A", "B", "C"],
"BCA": ["A", "B", "C"],
"B.Tech": ["A", "B", "C", "D"],
"BBA": ["A", "B"],
"MCA": ["A", "B"]
}

## Future Improvements
- Export to CSV
- Graphical analytics
- Login authentication

## Author
**GitHub:** https://github.com/nishukumaricsd24-web/student-record-system

## License
Created for learning and educational purposes.