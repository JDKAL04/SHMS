from django.db import models
from halls.models import Hall

class GrantAllocation(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.IntegerField()

class GrantExpenditure(models.Model):
    allocation = models.ForeignKey(GrantAllocation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()

class PettyExpense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()
