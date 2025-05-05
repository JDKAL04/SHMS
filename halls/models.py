from django.db import models
from django.conf import settings

class Hall(models.Model):
    name = models.CharField(max_length=100)
    is_new = models.BooleanField(default=True)

class Room(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    rent = models.DecimalField(max_digits=8, decimal_places=2)
    SHARING_CHOICES = [('single','Single'),('twin','Twin')]
    sharing_type = models.CharField(max_length=6, choices=SHARING_CHOICES)

class HallAmenity(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=6, decimal_places=2)

class ActionTakenReport(models.Model):
    hall = models.ForeignKey(
        Hall, on_delete=models.CASCADE, related_name='atrs'
    )
    date = models.DateTimeField(auto_now_add=True)
    report = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True,
        related_name='created_atrs'
    )

    def __str__(self):
        return f"ATR for {self.hall.name} at {self.date:%Y-%m-%d}"