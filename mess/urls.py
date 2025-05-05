# mess/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('',             views.messcharge_list,  name='messcharge_list'),
    path('new/',         views.messcharge_create,name='messcharge_create'),
    path('dues/',        views.student_dues,     name='student_dues'),
    path('cheques/',     views.mess_cheque_sheet,name='mess_cheque_sheet'),
]
