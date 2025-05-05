# shms/staff/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .models import TemporaryStaff, Attendance, Payroll,Staff
from .forms  import StaffForm, AttendanceForm
from datetime import date

# ---- Temporary Staff CRUD ----
def staff_form(request):
    """
    Create a new TemporaryStaff record.
    Also handles the URL name 'staff_create'.
    """
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff added successfully!")
            return redirect('staff:staff_list')
    else:
        form = StaffForm()

    return render(request, 'staff/staff_form.html', {
        'form': form
    })

def staff_list(request):
    """
    List all TemporaryStaff records.
    """
    staff_list = TemporaryStaff.objects.all()
    return render(request, 'staff/staff_list.html', {
        'staff_list': staff_list
    })


# ---- Attendance ----
def attendance_form(request):
    """
    Record attendance for a TemporaryStaff member.
    """
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Attendance recorded!")
            return redirect('staff:attendance_list')
    else:
        form = AttendanceForm()

    return render(request, 'staff/attendance_form.html', {
        'form': form
    })

def attendance_list(request):
    """
    Display all attendance records.
    """
    attendances = Attendance.objects.select_related('staff').all()
    return render(request, 'staff/attendance_list.html', {
        'attendances': attendances
    })


# ---- Payroll ----
def payroll_list(request):
    """
    Show computed payroll records.
    """
    payrolls = Payroll.objects.select_related('staff').all()
    return render(request, 'staff/payroll_list.html', {
        'payrolls': payrolls
    })

def payroll_cheques(request):
    """
    Render a page (or PDF) listing cheques for payroll.
    """
    payrolls = Payroll.objects.select_related('staff').all()
    return render(request, 'staff/payroll_cheques.html', {
        'payrolls': payrolls
    })

def payslip(request, pk):
    """
    Display (or PDF) the payslip for a specific payroll record.
    """
    payroll = get_object_or_404(Payroll, pk=pk)
    return render(request, 'staff/payslip.html', {
        'payroll': payroll
    })
    

def staff_delete(request, staff_id):
    staff = get_object_or_404(TemporaryStaff, id=staff_id)
    if request.method == 'POST':
        staff.delete()
        messages.success(request, 'Staff record deleted.')
        return redirect('staff:staff_list')
    return render(request, 'staff/staff_confirm_delete.html', {'staff': staff})

@role_required('staff_admin')
def staff_list(request):
    staffs = Staff.objects.all()               
    return render(request, 'staff/staff_list.html', {
        'staffs': staffs                         
    })

@role_required('staff_admin')
def staff_create(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff member added.')
            return redirect('staff:staff_list')    # ← must match your URL name
    else:
        form = StaffForm()

    return render(request, 'staff/staff_create.html', {'form': form})


@role_required('staff_admin')
def attendance_list(request):
    attendance_list = Attendance.objects.select_related('staff').all()
    return render(request, 'staff/attendance_list.html', {
        'attendance_list': attendance_list
    })

@role_required('staff_admin')
def attendance_create(request):
    form = AttendanceForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('staff:attendance_list')
    return render(request, 'staff/attendance_form.html', {'form': form})

@role_required('staff_admin')
def payroll_list(request):
    """
    Compute this month’s payroll: days present × daily_pay for each staff.
    """
    today = date.today()
    year, month = today.year, today.month

    payroll_items = []
    for staff in Staff.objects.all():
        days_present = Attendance.objects.filter(
            staff=staff,
            date__year=year,
            date__month=month,
            status='present'
        ).count()
        total_amount = days_present * staff.daily_pay
        payroll_items.append({
            'staff':        staff,
            'days_worked':  days_present,
            'total_pay':    total_amount
        })

    return render(request, 'staff/payroll_list.html', {
        'payroll_items': payroll_items,
        'year': year,
        'month': month,
    })