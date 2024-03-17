
from django.urls import path

from hostelapp import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('hostel/', views.hostel_page, name='hostel_page'),
    path('hostel/add/', views.add_hostel_form, name='add_hostel_form'),
    path('hostel/<int:hostel_id>/', views.hostel_detail, name='hostel_detail'),
    path('edit_hostel/<int:hostel_id>/', views.edit_hostel, name='edit_hostel'),
    path('add_floor/<int:hostel_id>/', views.add_floor, name='add_floor'),
    path('add_room/<int:hostel_id>/', views.add_room, name='add_room'),
    path('add_bed/<int:hostel_id>/', views.add_bed, name='add_bed'),
    path('get_rooms/', views.get_rooms, name='get_rooms'),
    path('update_hostel_status/', views.update_hostel_status, name='update_hostel_status'),
    path('get_floors/', views.get_floors, name='get_floors'),
    path('get_beds/', views.get_beds, name='get_beds'),
    path('user_registration/', views.user_registration, name='user_registration'),
    path('view_users/', views.view_users, name='view_users'),
    path('update_user_status/<int:user_id>/', views.update_user_status, name='update_user_status'),
    path('get_user_details/<int:user_id>/', views.get_user_details, name='get_user_details'),
    path('hostel_analytics/', views.hostel_analytics, name='hostel_analytics'),
    
   
   

]