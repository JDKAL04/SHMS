# app1/tests/test_forms.py
from django.test import TestCase
from .forms import StudentForm

class StudentFormTest(TestCase):
    def test_valid_data(self):
        form = StudentForm(data={
            'name': 'Bob',
            'roll_no': 'B002',
            'room_number': 102
        })
        self.assertTrue(form.is_valid())

    def test_room_number_invalid(self):
        form = StudentForm(data={
            'name': 'Bob',
            'roll_no': 'B002',
            'room_number': -5
        })
        self.assertFalse(form.is_valid())
        self.assertIn('room_number', form.errors)
