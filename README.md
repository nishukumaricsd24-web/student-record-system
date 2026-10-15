# Student Record Management System - Python + SQLite

A clean, menu-driven Command Line application to manage college student records. Built with Python and SQLite with strong input validation and error handling. Created as a college project and designed to be resume and interview ready.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![SQLite](https://img.shields.io/badge/SQLite-3-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

## 📖 Project Overview

The Student Record Management System allows users to add, view, search, update, and delete student records directly from the terminal. All records are stored permanently in a local SQLite database (`students.db`) and remain saved even after restarting the application.

This project was built in 4 phases:
- **Phase 1:** Core Python OOP - Student class + CLI menu
- **Phase 2:** SQLite integration for permanent storage
- **Phase 3:** Input validation, duplicate prevention & error handling
- **Phase 4:** Professional documentation for GitHub & internships

The application runs entirely in the VS Code terminal - no web, GUI or mobile framework required.

## ❓ Problem Statement

Many beginner college projects store data only in memory (Python lists), so all records are lost when the program closes. They also lack proper validation, allowing duplicate roll numbers, empty names, or invalid marks.

This project solves that by providing a persistent, validated, and error-proof system that handles real-world user mistakes without crashing.

## 🎯 Project Objectives

- To apply Object-Oriented Programming (OOP) concepts in Python
- To perform CRUD operations - Create, Read, Update, Delete
- To integrate SQLite for permanent data storage
- To implement robust input validation and error handling
- To build a clean, maintainable, and beginner-friendly codebase
- To make the project professional and showcase-ready for GitHub

## ✨ Key Features

- **Add Student** - Add new student with full validation
- **View All Students** - Display all records in readable format
- **Search Student** - Search by roll number
- **Update Student** - Update name, course, marks and roll number
- **Delete Student** - Delete with user confirmation
- **Permanent Storage** - All data saved in `students.db` using SQLite
- **Duplicate Prevention** - Roll number is PRIMARY KEY
- **Smart Validation** - Handles empty inputs, spaces, and invalid types
- **Error Handling** - Program never crashes on wrong input

## 🛠️ Technologies Used

| Technology | Purpose |
| :--- | :--- |
| **Python 3** | Core programming language |
| **SQLite 3** | Local database (built-in, no setup needed) |
| **VS Code** | Development & running the application |
| **Git & GitHub** | Version control |

> No external libraries or frameworks used. Only Python standard library.

## 📁 Project Folder Structure

This is the actual structure of the project. Student-Record-Management-System/
│
├── main.py # Main menu, user input & validation logic
├── student.py # Student class with __init__() and display() method
├── database.py # All SQLite operations (parameterized queries)
├── students.db # Local SQLite database file (auto-created)
├── .gitignore # Excludes DB and cache files from GitHub
└── README.md # Project documentation (this file)
**Optional files for future scope:**
- `requirements.txt` - (Optional) Not needed for this project as no external libraries are used
- `screenshots/` - (Optional) Folder to add terminal output screenshots for GitHub

## ⚙️ Installation Requirements

- Python 3.8 or above - Check with `python --version` or `python3 --version`
- VS Code or any code editor
- Git installed for GitHub push
- No pip install needed - `sqlite3` and `math` are built-in

## 🚀 Step-by-Step Setup Instructions

**1. Clone the repository**bash
git clone https://github.com/YOUR_USERNAME/Student-Record-Management-System.git
cd Student-Record-Management-System
**2. Verify Python installation**
bash
python --version
or
python3 --version
code

**3. Check files**
Make sure `main.py`, `student.py`, `database.py` and `.gitignore` are in the same folder.

**4. Run the application**
bash
python main.py
if above fails, try:python3 main.py
code

Copy
On first run, `students.db` will be created automatically and you will see:
`Database initialized successfully. (students.db ready)`

## ▶️ How to Run in VS Code

1. Open VS Code -> `File` -> `Open Folder` -> Select your project folder
2. Open Terminal: `View` -> `Terminal` or `Ctrl + ` `
3. Run: `python main.py`
4. Use the menu by entering numbers `1` to `6`

## 📋 How to Use Each Menu Option

You will see this menu after running:

===== Student Record Management System =====
Add Student

View All Students

Search Student

Update Student

Delete Student

Exit

Enter your choice:
code

Copy

| Option | What it does | Input Required |
| :--- | :--- | :--- |
| **1. Add Student** | Adds a new student | Roll Number, Name, Course, Marks |
| **2. View All Students** | Shows all saved records | No input |
| **3. Search Student** | Finds a student by roll number | Roll Number |
| **4. Update Student** | Updates existing record. Press Enter to keep old value | Roll Number to find + New values |
| **5. Delete Student** | Deletes after confirmation `y/n` | Roll Number |
| **6. Exit** | Safely exits the program | No input |

## 🛡️ Input Validation and Error Handling

| Validation | Rule | Error Message |
| :--- | :--- | :--- |
| **Roll Number** | Must be positive integer, unique | `Error: Roll number must be a positive integer!` / `Error: Student with Roll Number X already exists!` |
| **Name & Course** | Cannot be empty or only spaces, trimmed with `.strip()` | `Error: Name cannot be empty!` |
| **Marks** | Must be numeric and between 0-100 (0 and 100 included) | `Error: Marks must be between 0 and 100!` |
| **Search** | Empty search not allowed | `Error: Search query cannot be empty!` |
| **Update** | Validates all new fields before saving, prevents duplicate roll | `Error: Roll Number X already assigned to another student!` `Update cancelled.` |
| **Delete** | Asks for confirmation, checks if exists | `Are you sure you want to delete...? (y/n)` |
| **Menu** | Only 1-6 allowed, handles empty/invalid input | `Invalid choice! Please enter a number between 1 and 6.` |
| **Database** | All queries use `?` placeholders, wrapped in `try-except sqlite3.Error` | `Database Error: ...` without crashing |

## 💻 Sample Terminal Output

**Adding a student:**

===== Student Record Management System =====
Enter your choice: 1

--- Add Student ---
Enter Roll Number: 101
Enter Name: Nisha
Enter Course: CSE
Enter Marks (0-100): 85
Student added successfully!
code

Copy

**Viewing all students:**

--- View All Students ---
Total Students: 2

Roll Number : 101
Name : Nisha
Course : CSE
Marks : 85.0
-----------------------------------
Roll Number : 102
Name : Amit
Course : ECE
Marks : 92.0
-----------------------------------
code

Copy

**Handling duplicate roll number:**

Enter Roll Number: 101
Error: Student with Roll Number 101 already exists!
code

Copy

## 🧪 Test Cases and Expected Results

| Test Case | Input | Expected Result |
| :--- | :--- | :--- |
| Add valid student | Roll: 101, Name: Nisha, Course: CSE, Marks: 85 | `Student added successfully!` |
| Add duplicate roll | Roll: 101 again | `Error: Student with Roll Number 101 already exists!` |
| Empty name | Name: `""` or `"   "` | `Error: Name cannot be empty!` |
| Empty course | Course: `""` | `Error: Course cannot be empty!` |
| Non-numeric marks | Marks: `abc` | `Error: Marks must be a number!` |
| Marks below 0 | Marks: `-10` | `Error: Marks must be between 0 and 100!` |
| Marks above 100 | Marks: `105` | `Error: Marks must be between 0 and 100!` |
| Valid edge marks | Marks: `0` and `100` | `Student added successfully!` (both valid) |
| Search existing | Search: `101` | `Student Found:` + details |
| Search non-existent | Search: `999` | `Student with Roll Number 999 not found!` |
| Search empty | Search: `""` (press Enter) | `Error: Search query cannot be empty!` |
| Update valid | Update 101 -> Name: Nisha Verma | `Student record updated successfully!` |
| Update to duplicate roll | Update 102 -> New Roll: `101` | `Error: Roll Number 101 already assigned to another student!` |
| Update with invalid marks | Update 101 -> Marks: `150` | `Error: Marks must be between 0 and 100! Update cancelled.` |
| Delete confirm Yes | Delete 101 -> `y` | `Student deleted successfully!` |
| Delete cancel | Delete 101 -> `n` | `Deletion cancelled.` |
| Invalid menu choice | Choice: `9`, `abc`, `""` | `Invalid choice! Please enter a number between 1 and 6.` |

**Verify Persistence:**
1. Add 2 students and View All
2. Press `6` to Exit
3. Run `python main.py` again
4. Select `2. View All Students` - same records still appear

## 🔮 Future Improvements

- [ ] Export records to CSV / Excel
- [ ] Add file backup and restore
- [ ] Add sorting by marks / name / roll number
- [ ] Add attendance and grade calculation
- [ ] Build Web version using Flask / Django
- [ ] Build GUI version using Tkinter
- [ ] Add user authentication (Admin login)

## 👨‍💻 Author

**[Your Full Name]**
- GitHub: [@YourUsername](https://github.com/YourUsername)
- LinkedIn: [linkedin.com/in/your-profile](https://linkedin.com/in/your-profile)
- Email: `your.email@example.com`

> College Student | Aspiring Software Developer | Python Enthusiast

## 📄 License

This project is for educational purposes. Free to use and modify.
