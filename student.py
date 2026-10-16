# student.py - Defines the Student blueprint
class Student:
    """
    Student class to store details of a single student.
    Backward compatible - new fields have defaults.
    """
    def __init__(self, roll_number, name, course, marks, section="", phone="", email=""):
        self.roll_number = roll_number
        self.name = name
        self.course = course
        self.section = section
        self.phone = phone
        self.marks = marks
        self.email = email

    def display(self):
        print(f"Roll Number : {self.roll_number}")
        print(f"Name        : {self.name}")
        print(f"Course      : {self.course}")
        print(f"Section     : {self.section}")
        print(f"Phone       : {self.phone}")
        print(f"Marks       : {self.marks}")
        print(f"Email       : {self.email}")
        print("-" * 35)