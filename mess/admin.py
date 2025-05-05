from django.contrib import admin
from .models import MessCharge

@admin.register(MessCharge)
class MessChargeAdmin(admin.ModelAdmin):
    list_display = ('student','hall','month','amount')
    list_filter  = ('hall','month')
    search_fields= ('student__name',)
