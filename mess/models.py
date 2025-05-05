from django.db import models
from students.models import Student
from halls.models import Hall

class MessCharge(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    month = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
