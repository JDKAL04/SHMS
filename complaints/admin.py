from django.contrib import admin
from .models import Complaint, ActionTakenReport

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('student','hall','category','status','date')
    list_filter  = ('hall','category','status')
    search_fields= ('student__name','description')

@admin.register(ActionTakenReport)
class ATRAdmin(admin.ModelAdmin):
    list_display = ('complaint','status','created_on')
    search_fields= ('warden_notes',)
