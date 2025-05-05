# shms/complaints/urls.py

from django.urls import path
from . import views

app_name = 'complaints'

urlpatterns = [
    # form to create a new complaint
    path('new/', views.complaint_create, name='complaint_create'),
    # list all complaints
    path('',    views.complaint_list,   name='complaint_list'),
]