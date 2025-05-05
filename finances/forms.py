# finances/forms.py

from django import forms
from .models import GrantAllocation, GrantExpenditure, PettyExpense
from halls.models import Hall

class GrantAllocationForm(forms.ModelForm):
    class Meta:
        model = GrantAllocation
        fields = ['hall', 'year', 'amount']
        widgets = {
            'hall':   forms.Select(attrs={'class':'form-control'}),
            'year':   forms.NumberInput(attrs={'class':'form-control'}),
            'amount': forms.NumberInput(attrs={'class':'form-control', 'step':'0.01'}),
        }

class GrantExpenditureForm(forms.ModelForm):
    class Meta:
        model = GrantExpenditure
        fields = ['allocation', 'date', 'amount', 'description']
        widgets = {
            'allocation':  forms.Select(attrs={'class':'form-control'}),
            'date':        forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'amount':      forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),
            'description': forms.Textarea(attrs={'class':'form-control','rows':2}),
        }

class PettyExpenseForm(forms.ModelForm):
    class Meta:
        model = PettyExpense
        fields = ['date', 'amount', 'description']
        widgets = {
            'date':        forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'amount':      forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),
            'description': forms.Textarea(attrs={'class':'form-control','rows':2}),
        }
