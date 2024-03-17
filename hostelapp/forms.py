# forms.py

from django import forms

class AddHostelForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    address = forms.CharField(label='Address', widget=forms.Textarea(attrs={'rows': 3}))
    organisation = forms.CharField(label='Organisation', max_length=100, required=False, initial='Default Organisation')
    branch = forms.CharField(label='Branch', max_length=100, required=False, initial='Default Branch')
    total_floors = forms.IntegerField(label='Total Floors', required=False)
    total_rooms_per_floor = forms.IntegerField(label='Total Rooms per Floor', required=False)
    number_of_beds_per_room = forms.IntegerField(label='Number of Beds per Room', required=False)
    occupancy_rate_per_room = forms.FloatField(label='Occupancy Rate per Room', required=False)

