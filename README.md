# Student Record Management System

A simple application built with Python and SQLite to manage student records efficiently. Available as both CLI and professional Desktop GUI.

## Features

**Core:**
- Add new student records
- View all students
- Search by Roll Number OR Name
- Update student details (including Roll Number with duplicate check)
- Delete student records with confirmation
- Validations & duplicate prevention
- Persistent SQLite storage

**GUI (New in `gui.py`):**
- Modern dashboard layout with sidebar navigation
- Header, summary cards (Total Students / Database status)
- Student form with validation (Roll >0, Name/Course required, Marks 0-100)
- Tkinter Treeview table with alternating row colors, scrollbar, and auto-refresh
- Click a row to auto-populate form
- Search bar for roll number or name (partial match)
- Confirmation dialogs and success/error popups
- Resizable window, professional colors & fonts

## Technologies Used
- Python 3
- SQLite (students.db)
- Tkinter (built-in, no extra dependencies)
- Git and GitHub

## Project Structure
student-record-system/
├── main.py # CLI version (unchanged)
├── student.py # Student class
├── database.py # SQLite operations (reused by CLI & GUI)
├── gui.py # NEW: Tkinter GUI application
├── students.db # Created automatically on first run
├── .gitignore
└── README.md
## How to Run

### Option 1: GUI (Recommended)bash
python gui.py
code

### Option 2: CLI
bash
python main.py 
Both share the same `students.db` - records are interchangeable.

## How to Use GUI
1. Run `python gui.py`
2. Fill Roll Number, Name, Course, Marks and click **Add Student**
3. Click any row in the table to edit - change values and click **Update Student** (you can also change Roll Number)
4. Use search bar above table to search by roll or name, **View All** to reset
5. Select a row and click **Delete Student** -> confirm with Yes
6. **Clear Fields** resets the form

## Database
SQLite `students.db` with table `students(roll_no INTEGER PRIMARY KEY, name TEXT, course TEXT, marks REAL)`. Uses parameterized queries. Auto-created via `database.create_table()`.

## Future Improvements
- Export to CSV
- Graphical analytics
- Login authentication
- 3. Changed Files Summary


| File | Status | Details |
|------|--------|---------|
| gui.py | NEW | Separate GUI file. Reuses database.py and student.py. No duplicate DB or fake data. |
| README.md | UPDATED | Added GUI documentation and python gui.py command |
| main.py, student.py, database.py | UNCHANGED | Preserved for CLI compatibility as requested |
