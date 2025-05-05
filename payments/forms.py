# payments/forms.py

from django import forms
from .models import Payment, Cheque
from students.models import Student

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'amount', 'method']
        widgets = {
            'student': forms.Select(attrs={'class':'form-control'}),
            'date':    forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'amount':  forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),
            'method':  forms.Select(attrs={'class':'form-control'}),
        }

class ChequeForm(forms.ModelForm):
    class Meta:
        model = Cheque
        fields = ['payment', 'cheque_number', 'bank']
        widgets = {
            'payment':       forms.HiddenInput(),
            'cheque_number': forms.TextInput(attrs={'class':'form-control'}),
            'bank':          forms.TextInput(attrs={'class':'form-control'}),
            'date':          forms.DateInput(attrs={'class':'form-control','type':'date'}),
        }
