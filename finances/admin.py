from django.contrib import admin
from .models import GrantAllocation, GrantExpenditure, PettyExpense

@admin.register(GrantAllocation)
class GrantAllocationAdmin(admin.ModelAdmin):
    list_display = ('hall','year','amount')
    list_filter  = ('hall','year')

@admin.register(GrantExpenditure)
class GrantExpenditureAdmin(admin.ModelAdmin):
    list_display = ('allocation','date','amount')
    list_filter  = ('allocation__hall','date')

@admin.register(PettyExpense)
class PettyExpenseAdmin(admin.ModelAdmin):
    list_display = ('date','amount','description')
    list_filter  = ('date',)
