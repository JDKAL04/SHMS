# mess/forms.py

from django import forms
from .models import MessCharge
from halls.models import Hall
from students.models import Student

class MessChargeForm(forms.ModelForm):
    class Meta:
        model = MessCharge
        fields = ['student', 'hall', 'month', 'amount']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'hall':    forms.Select(attrs={'class': 'form-control'}),
            'month':   forms.DateInput(attrs={'class': 'form-control', 'type': 'month'}),
            'amount':  forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
