"""Seed the gradebook JSON file with sample records."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gradebook.service import add_course, add_grade, add_student, enroll
from gradebook.storage import DATA_FILE, load_data, save_data


def seed():
    """Create demo students, courses, and grades."""
    data = load_data()
    data["students"] = []
    data["courses"] = []
    data["enrollments"] = []
    save_data(data)

    student_1 = add_student("Alice")
    student_2 = add_student("Bob")
    student_3 = add_student("Charlie")

    add_course("CS101", "Intro to CS")
    add_course("MATH100", "Calculus")

    enroll(student_1, "CS101")
    enroll(student_2, "CS101")
    enroll(student_3, "MATH100")

    add_grade(student_1, "CS101", 95)
    add_grade(student_1, "CS101", 90)
    add_grade(student_2, "CS101", 88)
    add_grade(student_3, "MATH100", 80)

    print(f"Seed data created in {DATA_FILE}")


if __name__ == "__main__":
    seed()