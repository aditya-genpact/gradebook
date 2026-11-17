import unittest

from gradebook.service import add_course, add_grade, add_student, compute_average, enroll
from gradebook.storage import save_data


class TestService(unittest.TestCase):

    def setUp(self):
        save_data({
            "students": [],
            "courses": [],
            "enrollments": [],
        })

    def test_add_student(self):
        sid = add_student("Test User")
        self.assertTrue(sid > 0)

    def test_add_grade(self):
        student_id = add_student("Alice")
        add_course("CS101", "Intro to CS")
        enroll(student_id, "CS101")
        add_grade(student_id, "CS101", 95)
        add_grade(student_id, "CS101", 90)

        self.assertEqual(compute_average(student_id, "CS101"), 92.5)

    def test_compute_average(self):
        student_id = add_student("Alice")
        add_course("CS101", "Intro to CS")
        enroll(student_id, "CS101")
        add_grade(student_id, "CS101", 90)
        add_grade(student_id, "CS101", 95)

        avg = compute_average(student_id, "CS101")
        self.assertEqual(avg, 92.5)

    def test_invalid_average(self):
        with self.assertRaises(ValueError):
            compute_average(999, "ABC")


if __name__ == "__main__":
    unittest.main()