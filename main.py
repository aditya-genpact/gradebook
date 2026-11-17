import argparse
import logging

from gradebook.service import (
    add_course,
    add_grade,
    add_student,
    compute_average,
    compute_gpa,
    enroll,
    list_courses,
    list_enrollments,
    list_students,
)


def parse_grade(value):

    """Convert a grade string to a float and validate the allowed range."""

    try:
        grade = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Grade must be a number") from exc

    if grade < 0 or grade > 100:
        raise ValueError("Grade must be between 0 and 100")

    return grade


def _print_list(items, formatter):
    if not items:
        print("No records found.")
        return
    for item in items:
        print(formatter(item))


def main():
    """Run the command-line interface for the gradebook application."""
    
    parser = argparse.ArgumentParser(description="Gradebook CLI")
    subparsers = parser.add_subparsers(dest="command")

    student_parser = subparsers.add_parser("add-student", help="Add a new student")
    student_parser.add_argument("--name", required=True)

    course_parser = subparsers.add_parser("add-course", help="Add a new course")
    course_parser.add_argument("--code", required=True)
    course_parser.add_argument("--title", required=True)

    enroll_parser = subparsers.add_parser("enroll", help="Enroll a student in a course")
    enroll_parser.add_argument("--student-id", type=int, required=True)
    enroll_parser.add_argument("--course", required=True)

    grade_parser = subparsers.add_parser("add-grade", help="Add a grade to an enrollment")
    grade_parser.add_argument("--student-id", type=int, required=True)
    grade_parser.add_argument("--course", required=True)
    grade_parser.add_argument("--grade", required=True)

    list_parser = subparsers.add_parser("list", help="List records")
    list_parser.add_argument("entity", choices=["students", "courses", "enrollments"])
    list_parser.add_argument("--sort", choices=["name", "code"], default=None)

    avg_parser = subparsers.add_parser("avg", help="Compute a course average")
    avg_parser.add_argument("--student-id", type=int, required=True)
    avg_parser.add_argument("--course", required=True)

    gpa_parser = subparsers.add_parser("gpa", help="Compute a student's GPA")
    gpa_parser.add_argument("--student-id", type=int, required=True)

    args = parser.parse_args()

    try:
        if args.command == "add-student":
            student_id = add_student(args.name)
            print(f"Student created with ID {student_id}")

        elif args.command == "add-course":
            add_course(args.code, args.title)
            print("Course added")

        elif args.command == "enroll":
            enroll(args.student_id, args.course)
            print("Enrollment successful")

        elif args.command == "add-grade":
            grade = parse_grade(args.grade)
            add_grade(args.student_id, args.course, grade)
            print("Grade added")

        elif args.command == "list":
            if args.entity == "students":
                records = list_students()
                if args.sort == "name":
                    records = sorted(records, key=lambda student: student["name"].lower())
                _print_list(records, lambda student: f"{student['id']}: {student['name']}")
            elif args.entity == "courses":
                records = list_courses()
                if args.sort == "code":
                    records = sorted(records, key=lambda course: course["code"].lower())
                _print_list(records, lambda course: f"{course['code']}: {course['title']}")
            else:
                records = list_enrollments()
                _print_list(records, lambda enrollment: (
                    f"Student {enrollment['student_id']} -> {enrollment['course_code']} "
                    f"(grades: {enrollment['grades']})"
                ))

        elif args.command == "avg":
            average = compute_average(args.student_id, args.course)
            print(f"Average: {average:.2f}")

        elif args.command == "gpa":
            gpa = compute_gpa(args.student_id)
            print(f"GPA: {gpa:.2f}")

        else:
            parser.print_help()

    except Exception as exc:
        logging.exception("Command failed: %s", exc)
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()