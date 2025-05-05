# app1/tests/test_models.py
from django.test import TestCase
from shms import Student

class StudentModelTest(TestCase):
    def setUp(self):
        # runs before each test
        self.student = Student.objects.create(
            name="Alice",
            roll_no="A001",
            room_number=101
        )

    def test_str_method(self):
        self.assertEqual(str(self.student), "Alice (A001)")

    def test_room_number_positive(self):
        self.assertGreater(self.student.room_number, 0)
