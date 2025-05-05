# shms/staff/models.py

import datetime
from django.db import models

class Staff(models.Model):
    name      = models.CharField(max_length=100)
    daily_pay = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

class TemporaryStaff(models.Model):
    name       = models.CharField(max_length=255)
    daily_wage = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent',  'Absent'),
    )

    staff  = models.ForeignKey(TemporaryStaff, on_delete=models.CASCADE)
    date   = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Present',     # ← every old row becomes “Present”
    )

    def __str__(self):
        return f"{self.staff.name} – {self.date} – {self.status}"

class Payroll(models.Model):
    staff  = models.ForeignKey(TemporaryStaff, on_delete=models.CASCADE)

    # ← GIVE DEFAULTS so Django won’t prompt you:
    month  = models.IntegerField(
        default=datetime.date.today().month,  
        help_text="Numeric month (1–12)."
    )
    year   = models.IntegerField(
        default=datetime.date.today().year,   
        help_text="Four-digit year."
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.staff.name} – {self.month}/{self.year} – ₹{self.amount}"