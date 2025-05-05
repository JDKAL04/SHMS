from django.contrib import admin
from .models import Payment, Cheque

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student','date','amount','method')
    list_filter  = ('method','date')

@admin.register(Cheque)
class ChequeAdmin(admin.ModelAdmin):
    list_display = ('payment','cheque_number','bank')
    search_fields= ('cheque_number','bank')
