# shms/staff/urls.py

from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('',                views.staff_list,       name='staff_list'),
    path('add/',            views.staff_create,     name='staff_create'),
    path('staff/<int:staff_id>/delete/', views.staff_delete, name='staff_delete'),

    # Attendance
    path('attendance/new/',  views.attendance_create,  name='attendance_create'),
    path('attendance/',      views.attendance_list,  name='attendance_list'),

    # Payroll
    path('payroll/',         views.payroll_list,     name='payroll_list'),
    path('payroll/cheques/', views.payroll_cheques,  name='payroll_cheques'),
    path('payslip/<int:pk>/',views.payslip,          name='payslip'),
]