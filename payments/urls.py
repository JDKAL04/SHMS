# payments/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('',            views.payment_list,    name='payment_list'),
    path('new/',        views.payment_create,  name='payment_create'),
    path('cheque/<int:pk>/', views.cheque_create, name='cheque_create'),
    path('overview/',   views.dues_overview,   name='dues_overview'),
    path('payment/<int:payment_id>/cheque/', views.payment_cheque, name='payment_cheque'),
    path('pay-dues/', views.pay_dues, name='pay_dues'),
    path('dues-overview/', views.dues_overview, name='dues_overview'),
    
]
