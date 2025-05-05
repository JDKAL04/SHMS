# shms/complaints/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Complaint
from .forms import ComplaintForm

def complaint_create(request):
    """
    Display a form to submit a new complaint, save it, and redirect to list.
    """
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = request.user.student
            complaint.save()
            messages.success(request, "Your complaint has been submitted.")
            return redirect('complaints:complaint_list')
    else:
        form = ComplaintForm()

    return render(request, 'complaints/complaint_form.html', {
        'form': form
    })


def complaint_list(request):
    """
    Show all complaints (or filter to this user if needed).
    """
    if request.user.profile.role == 'student':
        qs = Complaint.objects.filter(student__user=request.user)
    else:
        qs = Complaint.objects.all()

    return render(request, 'complaints/complaint_list.html', {
        'complaints': qs
    })