# Student Record Management System

A simple command-line application built with Python and SQLite to manage student records efficiently.

## Features

- Add new student records
- View all students
- Search for a student
- Update student details
- Delete student records
- Validate student inputs
- Prevent duplicate roll numbers
- Handle invalid inputs and database errors
- Store records persistently using SQLite

## Technologies Used

- Python
- SQLite
- Git and GitHub
- Visual Studio Code

## Project Structure

```text
student-record-system/
├── main.py
├── student.py
├── database.py
├── .gitignore
└── README.md
```

The `students.db` database file is created locally when the application initializes the database.

## How to Run

1. Install Python 3.
2. Clone the repository:

   ```bash
   git clone https://github.com/nishukumaricsd24-web/student-record-system.git
   ```

3. Open the project folder in VS Code.
4. Open the terminal in the project directory.
5. Run:

   ```bash
   python main.py
   ```

## How to Use

Follow the menu displayed in the terminal to add, view, search, update, or delete student records.

Enter valid student details when prompted. The application validates inputs and displays messages for invalid entries.

## Database

SQLite is used to store student records locally. Records remain saved when the application closes and restarts.

## Future Improvements

- Add a graphical user interface
- Export student records to CSV
- Add login and authentication
- Create a web-based version

## Author

**Name:** Your Name

**GitHub:** https://github.com/nishukumaricsd24-web

## License

This project was created for learning and educational purposes.