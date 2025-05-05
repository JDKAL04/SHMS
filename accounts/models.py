# accounts/models.py
from django.db import models
from django.contrib.auth.models import User


ROLE_CHOICES = [
    ('student',       'Student'),
    ('hall_clerk',    'Hall Clerk'),
    ('mess_manager',  'Mess Manager'),
    ('warden',        'Hall Warden'),
    ('finance_officer','Finance Officer'),
    ('staff_admin',   'Staff Admin'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


    def __str__(self):
        return f"{self.user.username} ({self.role})"
