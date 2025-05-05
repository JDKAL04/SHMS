# shms/staff/admin.py

from django.contrib import admin
from .models import TemporaryStaff, Attendance, Payroll

@admin.register(TemporaryStaff)
class TemporaryStaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'daily_wage')
    search_fields = ('name',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('staff', 'date', 'status')
    list_filter  = ('date', 'status')
    search_fields = ('staff__name',)
    date_hierarchy = 'date'


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('staff', 'month', 'year', 'amount')
    list_filter  = ('month', 'year')
    search_fields = ('staff__name',)
    # Removed invalid date_hierarchy setting for Payroll