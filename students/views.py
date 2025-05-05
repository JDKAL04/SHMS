# shms/students/views.py

from django.shortcuts               import render, redirect, get_object_or_404
from django.contrib                 import messages
from django.contrib.auth.decorators import login_required
from django.db.models               import Sum

from accounts.decorators            import role_required
from .models                        import Student, Admission
from .forms                         import StudentForm, AdmissionForm
from mess.models                    import MessCharge
from core.utils                     import render_to_pdf
from halls.models                   import HallAmenity


@role_required('hall_clerk')
def student_list(request):
    """Hall clerk: list all students."""
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})


@role_required('hall_clerk')
def student_create(request):
    """Hall clerk: add a new student."""
    if request.method == 'POST':
        if request.method == 'POST':
         form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added!')
            return redirect('students:student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form})


@role_required('hall_clerk')
def admission_list(request):
    """Hall clerk: view all admissions."""
    admissions = Admission.objects.select_related('student','hall','room').all()
    return render(request, 'students/admission_list.html', {'admissions': admissions})


@role_required('hall_clerk')
def admission_create(request):
    """Hall clerk: record a new admission."""
    if request.method == 'POST':
        form = AdmissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Admission recorded!')
            return redirect('students:admission_list')
    else:
        form = AdmissionForm()
    return render(request, 'students/admission_form.html', {'form': form})


@role_required('student')
def my_admissions(request):
    """Student: view only your own admissions."""
    student = Student.objects.filter(user=request.user).first()
    if not student:
        messages.error(request, "Your account isn't linked to a student profile.")
        return redirect('home')
    admissions = Admission.objects.filter(student=student)
    return render(request, 'students/my_admissions.html', {'admissions': admissions})


@role_required('student')
def my_dues(request):
    """Student: view your mess charges + room rent due."""
    student = Student.objects.filter(user=request.user).first()
    if not student:
        messages.error(request, "Your account isn't linked to a student profile.")
        return redirect('home')

    # Sum mess charges
    mess_total = MessCharge.objects.filter(student=student).aggregate(total=Sum('amount'))['total'] or 0

    # Room rent from admission
    admission = Admission.objects.filter(student=student).select_related('room').first()
    rent_amount = admission.room.rent if admission else 0
    # sum all amenities for this student’s hall
    amenity_total = (
    HallAmenity.objects
        .filter(hall=admission.hall)
        .aggregate(total=Sum('fee'))['total']
    or 0
)
    total_due = mess_total + rent_amount + amenity_total

    return render(request, 'students/my_dues.html', {
    'mess_total': mess_total,
    'rent_amount': rent_amount,
    'amenity_total': amenity_total,
    'total_due': total_due,
})
    

@role_required('hall_clerk')
def admission_letter(request, pk):
    admission = Admission.objects.select_related('student','hall','room').get(pk=pk)
    context = {'adm': admission}
    return render_to_pdf(
        'students/admission_letter.html',
        context,
        filename=f'admission_letter_{admission.pk}.pdf'
    )
