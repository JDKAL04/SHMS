# payments/views.py

from django.shortcuts import render, redirect, get_object_or_404
from students.models import Student
from accounts.decorators import role_required
from django.contrib import messages
from .models import Payment, Cheque
from .forms import PaymentForm, ChequeForm
from django.db.models import Sum
from datetime import date
from core.utils import render_to_pdf
from django.contrib.auth.decorators import login_required
from mess.models            import MessCharge
from halls.models           import HallAmenity

def payment_list(request):
    payments = Payment.objects.select_related('student').order_by('-date')
    return render(request, 'payments/payment_list.html', {'payments': payments})

def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            messages.success(request, 'Payment recorded.')
            if payment.method == Payment.METHOD_CHEQUE:
                return redirect('cheque_create', pk=payment.pk)
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'payments/payment_form.html', {'form': form})

def cheque_create(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        form = ChequeForm(request.POST)
        if form.is_valid():
            cheque = form.save()
            messages.success(request, 'Cheque recorded.')
            # TODO: render a printable cheque template
            return redirect('payment_list')
    else:
        form = ChequeForm(initial={'payment': payment})
    return render(request, 'payments/cheque_form.html', {'form': form, 'payment': payment})


@role_required('hall_clerk','finance_officer','warden')
def dues_overview(request):
    # For each student compute total dues and total payments
    from mess.models import MessCharge
    from halls.models import HallAmenity, Room
    from django.db.models import Sum

    students = Student.objects.all()
    overview = []
    for s in students:
        # mess total
        mess_total = MessCharge.objects.filter(student=s).aggregate(sum=Sum('amount'))['sum'] or 0
        # rent & amenities from admission
        admission = getattr(s, 'admission', None)
        rent = admission.room.rent if admission else 0
        amenity = sum(a.fee for a in HallAmenity.objects.filter(hall=admission.hall)) if admission else 0
        total_due = mess_total + rent + amenity

        # payments total
        paid = Payment.objects.filter(student=s).aggregate(sum=Sum('amount'))['sum'] or 0
        balance = total_due - paid

        overview.append({
            'student': s,
            'due':     total_due,
            'paid':    paid,
            'balance': balance,
        })
    return render(request, 'payments/dues_overview.html', {'overview': overview})

@role_required('hall_clerk')
def student_dues(request):
    payments = Payment.objects.select_related('student').all()
    return render(request, 'payments/payment_list.html', {'payments': payments})

@login_required
@role_required('hall_clerk','finance_officer','warden')
def payment_create(request):
    form = PaymentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('student_dues')
    return render(request, 'payments/payment_form.html', {'form': form})

@role_required('finance_officer','warden')
def cheque_list(request):
    cheques = Cheque.objects.all()
    return render(request, 'payments/cheque_list.html', {'cheques': cheques})

@role_required('finance_officer')
def cheque_create(request):
    form = ChequeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cheque_list')
    return render(request, 'payments/cheque_form.html', {'form': form})


@role_required('finance_officer','warden')
def payment_cheque(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render_to_pdf('payments/cheque.html', {'payment': payment})

@login_required
@role_required('student')
def pay_dues(request):
    # 1) find this student
    student = get_object_or_404(Student, user=request.user)

    # 2) calculate totals
    mess_total = (MessCharge.objects
                  .filter(student=student)
                  .aggregate(sum=Sum('amount'))['sum'] or 0)

    admission = getattr(student, 'admission', None)
    rent = admission.room.rent if admission else 0
    amenity = sum(a.fee for a in HallAmenity.objects.filter(hall=admission.hall)) if admission else 0

    total_due = mess_total + rent + amenity
    paid      = (Payment.objects
                 .filter(student=student)
                 .aggregate(sum=Sum('amount'))['sum'] or 0)
    balance   = total_due - paid

    # 3) render using the same template, but with only one record
    context = {
      'overview': [{
         'student': student,
         'due':     total_due,
         'paid':    paid,
         'balance': balance,
      }]
    }
    return render(request, 'payments/dues_overview.html', context)