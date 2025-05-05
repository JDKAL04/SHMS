# shms/students/models.py

from django.db import models
from django.contrib.auth.models import User
from halls.models import Hall, Room

class Student(models.Model):
    # ← this line is new
    user    = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Link to the User account"
    )
    name    = models.CharField(max_length=100)
    address = models.TextField()
    phone   = models.CharField(max_length=15)
    photo   = models.ImageField(upload_to='photos/')

    def __str__(self):
        return self.name

class Admission(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    hall    = models.ForeignKey(Hall, on_delete=models.PROTECT)
    room    = models.ForeignKey(Room, on_delete=models.PROTECT)
    date    = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} → {self.hall.name} / {self.room.number}"
    
mess_manager = models.ForeignKey(
    'auth.User',
    on_delete=models.SET_NULL,
    null=True, blank=True,
    help_text="Who collects this student’s mess charges"
)
