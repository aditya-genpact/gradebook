class Student:
    """Represents a student in the gradebook."""

    def __init__(self, student_id, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Student name cannot be empty")

        self.id = student_id
        self.name = name.strip()

    def __str__(self):
        return f"Student(id={self.id}, name='{self.name}')"


class Course:
    """Represents a course offered in the gradebook."""

    def __init__(self, code, title):
        if not isinstance(code, str) or not code.strip():
            raise ValueError("Course code cannot be empty")

        if not isinstance(title, str) or not title.strip():
            raise ValueError("Course title cannot be empty")

        self.code = code.strip()
        self.title = title.strip()

    def __str__(self):
        return f"Course(code='{self.code}', title='{self.title}')"


class Enrollment:
    """Represents a student's enrollment in a course."""

    def __init__(self, student_id, course_code, grades=None):
        self.student_id = student_id
        self.course_code = course_code
        self.grades = list(grades) if grades else []

        for grade in self.grades:
            self._validate_grade(grade)

    @staticmethod
    def _validate_grade(grade):
        if not isinstance(grade, (int, float)):
            raise ValueError("Grade must be numeric")

        if grade < 0 or grade > 100:
            raise ValueError("Grade must be between 0 and 100")

    def __str__(self):
        return (
            f"Enrollment(student_id={self.student_id}, "
            f"course_code='{self.course_code}', "
            f"grades={self.grades})"
        )