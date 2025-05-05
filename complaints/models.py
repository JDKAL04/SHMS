from django.db import models
from students.models import Student
from halls.models import Hall

class Complaint(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Open')

# complaints/models.py

class ActionTakenReport(models.Model):
    complaint    = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    report       = models.TextField()
    created_on   = models.DateTimeField(auto_now_add=True)

    # ←— add this:
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('R', 'Rejected'),
    ]
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='P',
        help_text="Current status of this ATR"
    )

    def __str__(self):
        return f"ATR for {self.complaint} ({self.get_status_display()})"

