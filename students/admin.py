from django.contrib import admin
from .models import Student, Admission

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search_fields = ('name', 'phone')

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'hall', 'room', 'date')
    list_filter  = ('hall', 'date')
    search_fields= ('student__name',)
