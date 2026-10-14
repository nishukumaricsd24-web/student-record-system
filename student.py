# student.py - Defines the Student blueprint

class Student:
    """
    Student class to store details of a single student.
    """
    def __init__(self, roll_number, name, course, marks):
        # Initialize attributes using self
        self.roll_number = roll_number  # Integer - Unique ID
        self.name = name                # String
        self.course = course            # String
        self.marks = marks              # Float/Integer 0-100

    def display(self):
        """Display all details of the student in a readable format."""
        print(f"Roll Number : {self.roll_number}")
        print(f"Name        : {self.name}")
        print(f"Course      : {self.course}")
        print(f"Marks       : {self.marks}")
        print("-" * 35)
