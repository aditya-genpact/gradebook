<<<<<<< HEAD
# gradebook
=======
# Gradebook CLI

A small Python project for tracking students, courses, enrollments, and grades via a CLI.

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

2. Install dependencies (none are required for the basic project):

```bash
python -m pip install --upgrade pip
```

## Seed sample data

```bash
python scripts/seed.py
```

This creates sample data in `data/gradebook.json`.

## Example CLI usage

```bash
python main.py add-student --name "Dana"
python main.py add-course --code CS101 --title "Intro to CS"
python main.py enroll --student-id 1 --course CS101
python main.py add-grade --student-id 1 --course CS101 --grade 95
python main.py list students
python main.py list courses --sort code
python main.py avg --student-id 1 --course CS101
python main.py gpa --student-id 1
```

Example expected output:

```text
Student created with ID 1
Course added
Enrollment successful
Grade added
Average: 92.50
GPA: 92.50
```

## Design decisions & limitations

- The project stores its data in a JSON file so it stays simple and easy to inspect.
- Validation checks are intentionally lightweight and focused on common errors such as empty names, invalid grades, or missing records.
- This version does not include database-backed persistence or authentication; it is designed as a learning-focused CLI.
- GPA is calculated as the simple mean of the student's course averages, which matches the assignment requirement.
>>>>>>> d65a418 (Initial gradebook project)
