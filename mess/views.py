# mess/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date
from .models import MessCharge
from .forms import MessChargeForm
from halls.models import Hall, HallAmenity
from students.models import Student
from halls.models import Room
from core.utils import render_to_pdf
from accounts.decorators import role_required


def messcharge_list(request):
    charges = MessCharge.objects.select_related('student','hall').order_by('-month')
    return render(request, 'mess/messcharge_list.html', {'charges': charges})

def messcharge_create(request):
    if request.method == 'POST':
        form = MessChargeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mess charge recorded.')
            return redirect('messcharge_list')
    else:
        form = MessChargeForm()
    return render(request, 'mess/messcharge_form.html', {'form': form})

def student_dues(request):
    # Compute dues per student for the latest month or filter by month param
    month = request.GET.get('month')
    if month:
        # parse YYYY-MM
        year, mon = map(int, month.split('-'))
    else:
        today = date.today()
        year, mon = today.year, today.month

    # Gather all students with a MessCharge for that month
    charges = MessCharge.objects.filter(month__year=year, month__month=mon)
    dues_list = []
    for ch in charges:
        student = ch.student
        # room rent
        admission = student.admission if hasattr(student, 'admission') else None
        rent = admission.room.rent if admission else 0
        # amenity fees: sum of hall amenities
        amenity_total = sum(a.fee for a in HallAmenity.objects.filter(hall=ch.hall))
        total_due = float(ch.amount) + float(rent) + float(amenity_total)
        dues_list.append({
            'student': student,
            'hall':    ch.hall,
            'mess':    ch.amount,
            'rent':    rent,
            'amenity': amenity_total,
            'total':   total_due,
        })

    return render(request, 'mess/student_dues.html', {
        'dues_list': dues_list,
        'year': year, 'month': mon,
    })

def mess_cheque_sheet(request):
    # group by manager
    managers = {}
    for c in MessCharge.objects.select_related('student__mess_manager'):
        mgr = c.student.mess_manager
        managers.setdefault(mgr, []).append(c)
    return render_to_pdf(
        'mess/cheque_sheet.html',
        {'managers': managers},
        filename='mess_cheques.pdf'
    )
    

@role_required('mess_manager')
def messcharge_create(request):
    form = MessChargeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('messcharge_list')
    return render(request, 'mess/messcharge_form.html', {'form': form})

@role_required('mess_manager')
def messcharge_list(request):
    charges = MessCharge.objects.select_related('student').all()
    return render(request, 'mess/messcharge_list.html', {'charges': charges})

@role_required('mess_manager')
def mess_cheque_sheet(request):
    managers = {}
    for c in MessCharge.objects.select_related('student__mess_manager'):
        mgr = c.student.mess_manager
        managers.setdefault(mgr, []).append(c)
    return render_to_pdf('mess/cheque_sheet.html', {'managers': managers}, 'mess_cheques.pdf')