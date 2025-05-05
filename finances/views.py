# finances/views.py

from django.shortcuts    import render, redirect
from django.contrib      import messages
from django.db.models    import Sum

from accounts.decorators import role_required
from core.utils          import render_to_pdf

from .models             import GrantAllocation, GrantExpenditure, PettyExpense
from .forms              import GrantAllocationForm, GrantExpenditureForm, PettyExpenseForm

@role_required('finance_officer', 'warden')
def allocation_list(request):
    allocs = GrantAllocation.objects.select_related('hall').all()
    return render(request, 'finances/allocation_list.html', {'allocations': allocs})

@role_required('finance_officer', 'warden')
def allocation_create(request):
    form = GrantAllocationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Grant allocated.')
        return redirect('allocation_list')
    return render(request, 'finances/allocation_form.html', {'form': form})

@role_required('finance_officer', 'warden')
def expenditure_create(request):
    form = GrantExpenditureForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Expenditure recorded.')
        return redirect('allocation_list')
    return render(request, 'finances/expenditure_form.html', {'form': form})

@role_required('finance_officer', 'warden')
def pettyexpense_list(request):
    expenses = PettyExpense.objects.order_by('-date')
    return render(request, 'finances/pettyexpense_list.html', {'expenses': expenses})

@role_required('finance_officer', 'warden')
def pettyexpense_create(request):
    form = PettyExpenseForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Petty expense logged.')
        return redirect('pettyexpense_list')
    return render(request, 'finances/pettyexpense_form.html', {'form': form})

@role_required('finance_officer', 'warden')
def allocation_report(request):
    allocs = GrantAllocation.objects.select_related('hall').all()
    report = []
    for a in allocs:
        spent  = GrantExpenditure.objects.filter(allocation=a).aggregate(total=Sum('amount'))['total'] or 0
        petty  = PettyExpense.objects.aggregate(total=Sum('amount'))['total'] or 0
        balance = a.amount - spent - petty
        report.append({
            'hall':      a.hall,
            'year':      a.year,
            'allocated': a.amount,
            'spent':     spent,
            'petty':     petty,
            'balance':   balance,
        })
    return render(request, 'finances/allocation_report.html', {'report': report})

@role_required('finance_officer', 'warden')
def grant_cheque_sheet(request):
    allocs = GrantAllocation.objects.select_related('hall').all()
    return render_to_pdf(
        'finances/grant_cheque_sheet.html',
        {'allocs': allocs},
        filename='grant_cheques.pdf'
    )
