import logging

from .storage import load_data, save_data


def _validate_student_name(name):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Student name cannot be empty")
    return name.strip()


def _validate_course(code, title):
    if not isinstance(code, str) or not code.strip():
        raise ValueError("Course code cannot be empty")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Course title cannot be empty")
    return code.strip(), title.strip()


def _validate_grade(grade):
    if not isinstance(grade, (int, float)):
        raise ValueError("Grade must be numeric")
    if grade < 0 or grade > 100:
        raise ValueError("Grade must be between 0 and 100")
    return float(grade)


def _student_exists(data, student_id):
    return any(student["id"] == student_id for student in data["students"])


def _course_exists(data, course_code):
    return any(course["code"] == course_code for course in data["courses"])


def add_student(name):
    """Create a new student record and return its id."""
    cleaned_name = _validate_student_name(name)
    data = load_data()

    student_id = max((student["id"] for student in data["students"]), default=0) + 1
    data["students"].append({"id": student_id, "name": cleaned_name})

    save_data(data)
    logging.info("Added student %s with id %s", cleaned_name, student_id)
    return student_id


def add_course(code, title):
    """Create a new course record."""
    clean_code, clean_title = _validate_course(code, title)
    data = load_data()

    if any(course["code"] == clean_code for course in data["courses"]):
        raise ValueError(f"Course {clean_code} already exists")

    data["courses"].append({"code": clean_code, "title": clean_title})
    save_data(data)
    logging.info("Added course %s (%s)", clean_code, clean_title)


def enroll(student_id, course_code):
    """Enroll a student in a course."""
    data = load_data()

    if not _student_exists(data, student_id):
        raise ValueError(f"Student {student_id} not found")
    if not _course_exists(data, course_code):
        raise ValueError(f"Course {course_code} not found")
    if any(
        enrollment["student_id"] == student_id and enrollment["course_code"] == course_code
        for enrollment in data["enrollments"]
    ):
        raise ValueError(f"Student {student_id} is already enrolled in {course_code}")

    data["enrollments"].append({
        "student_id": student_id,
        "course_code": course_code,
        "grades": [],
    })

    save_data(data)
    logging.info("Enrolled student %s in %s", student_id, course_code)


def add_grade(student_id, course_code, grade):
    """Add a grade for a specific student/course enrollment."""
    data = load_data()
    numeric_grade = _validate_grade(grade)

    for enrollment in data["enrollments"]:
        if (
            enrollment["student_id"] == student_id
            and enrollment["course_code"] == course_code
        ):
            enrollment["grades"].append(numeric_grade)
            save_data(data)
            logging.info("Added grade %s to student %s in %s", numeric_grade, student_id, course_code)
            return

    raise ValueError("Enrollment not found")


def list_students():
    """Return all students sorted by name."""
    data = load_data()
    return sorted(data["students"], key=lambda student: student["name"].lower())


def list_courses():
    """Return all courses sorted by code."""
    data = load_data()
    return sorted(data["courses"], key=lambda course: course["code"].lower())


def list_enrollments():
    """Return all enrollment records."""
    data = load_data()
    return sorted(
        data["enrollments"],
        key=lambda enrollment: (enrollment["student_id"], enrollment["course_code"]),
    )


def compute_average(student_id, course_code):
    """Return the average grade for a student in a course."""
    data = load_data()

    if not _student_exists(data, student_id):
        raise ValueError(f"Student {student_id} not found")
    if not _course_exists(data, course_code):
        raise ValueError(f"Course {course_code} not found")

    for enrollment in data["enrollments"]:
        if (
            enrollment["student_id"] == student_id
            and enrollment["course_code"] == course_code
        ):
            grades = enrollment["grades"]
            if not grades:
                return 0
            return sum(grades) / len(grades)

    raise ValueError("Enrollment not found")


def compute_gpa(student_id):
    """Return the grade-point average across all courses for a student."""
    data = load_data()

    if not _student_exists(data, student_id):
        raise ValueError(f"Student {student_id} not found")

    averages = [
        compute_average(student_id, enrollment["course_code"])
        for enrollment in data["enrollments"]
        if enrollment["student_id"] == student_id
    ]

    if not averages:
        return 0

    return sum(averages) / len(averages)