# shms/students/urls.py

from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('',                          views.student_list,      name='student_list'),
    path('create/',                   views.student_create,    name='student_create'),
    path('admissions/',               views.admission_list,    name='admission_list'),
    path('admissions/create/',        views.admission_create,  name='admission_create'),
    path('my-admissions/',            views.my_admissions,     name='my_admissions'),
    path('admission/<int:pk>/letter/',views.admission_letter,  name='admission_letter'),
    path('my-dues/',                  views.my_dues,           name='my_dues'),
]