from django import forms
from .models import Hall, Room
from .models import ActionTakenReport

class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = ['name', 'is_new']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_new': forms.CheckboxInput(),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['hall', 'number', 'sharing_type', 'rent']
        widgets = {
            'hall': forms.Select(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'sharing_type': forms.Select(attrs={'class': 'form-control'}),
            'rent': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
class ActionTakenReportForm(forms.ModelForm):
    class Meta:
        model = ActionTakenReport
        fields = ['report']
