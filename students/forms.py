# students/forms.py

from django import forms
from .models import Student, Admission

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'address', 'phone', 'photo']
        widgets = {
            'name':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'photo':   forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ['student', 'hall', 'room']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'hall':    forms.Select(attrs={'class': 'form-control', 'id': 'hall-select'}),
            'room':    forms.Select(attrs={'class': 'form-control', 'id': 'room-select'}),
        }
