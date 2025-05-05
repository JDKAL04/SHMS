from django.urls import path
from . import views

urlpatterns = [
    path('allocations/',    views.allocation_list,      name='allocation_list'),
    path('allocations/new/',views.allocation_create,    name='allocation_create'),
    path('expenditure/new/', views.expenditure_create,   name='expenditure_create'),
    path('petty/',          views.pettyexpense_list,    name='pettyexpense_list'),
    path('petty/new/',      views.pettyexpense_create,  name='pettyexpense_create'),
    path('report/',         views.allocation_report,    name='allocation_report'),
    path('grant-cheques/',  views.grant_cheque_sheet,   name='grant_cheque_sheet'),
]
