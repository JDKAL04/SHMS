from django.urls import path
from . import views

app_name = 'halls'

urlpatterns = [
    path('', views.hall_list, name='hall_list'),
    path('create/', views.hall_create, name='hall_create'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/new/', views.room_create, name='room_create'),
    path('rooms/hall/<int:hall_id>/', views.room_list, name='room_list_by_hall'),
    path('<int:hall_id>/occupancy/', views.hall_occupancy, name='hall_occupancy'),
    path('overall/',           views.overall_occupancy,     name='overall_occupancy'),
    path("<int:hall_id>/occupancy/", views.hall_occupancy,   name="hall_occupancy"),
    path('hall/<int:hall_id>/atr/create/', views.atr_create, name='atr_create'),
    path("<int:hall_id>/atr/create/", views.atr_create, name="atr_create"),
    path("<int:hall_id>/atr/",        views.atr_list,   name="atr_list"),
]

