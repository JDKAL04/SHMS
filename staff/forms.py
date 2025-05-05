# shms/staff/forms.py

from django import forms
from .models import TemporaryStaff, Attendance, Staff

class StaffForm(forms.ModelForm):
    class Meta:
        model = TemporaryStaff
        fields = ['name', 'daily_wage']
        widgets = {
            'name':       forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name'}),
            'daily_wage': forms.NumberInput(attrs={'class':'form-control', 'step':'0.01'}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['staff', 'date', 'status']
        widgets = {
            'staff':  forms.Select(attrs={'class':'form-control'}),
            'date':   forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'status': forms.Select(attrs={'class':'form-control'}),
        }
        
class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        # explicitly list the fields you want on your add‐staff form:
        fields = [
            'name',
            'daily_pay',   # ← make sure this is here!
            # any other fields you need…
        ]
        widgets = {
            'name':       forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name'}),
            'daily_pay': forms.NumberInput(attrs={'class':'form-control', 'step':'0.01'}),
        }