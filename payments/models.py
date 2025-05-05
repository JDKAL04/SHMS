from django.db import models
from students.models import Student

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    METHOD_CHOICES = [('cash','Cash'),('cheque','Cheque')]
    method = models.CharField(max_length=6, choices=METHOD_CHOICES)

class Cheque(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    cheque_number = models.CharField(max_length=50)
    bank = models.CharField(max_length=100)
