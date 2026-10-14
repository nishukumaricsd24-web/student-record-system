# student.py - Defines the Student blueprint


class Student:
    """Store details for a single student."""

    def __init__(self, roll_number, name, course, marks):
        self.roll_number = roll_number
        self.name = name
        self.course = course
        self.marks = marks

    def display(self):
        """Display all details of the student in a readable format."""
        print(f"Roll Number : {self.roll_number}")
        print(f"Name        : {self.name}")
        print(f"Course      : {self.course}")
        print(f"Marks       : {self.marks}")
        print("-" * 35)
