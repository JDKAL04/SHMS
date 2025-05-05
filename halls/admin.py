from django.contrib import admin
from .models import Hall, Room, HallAmenity

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_new')
    search_fields = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hall', 'number', 'sharing_type', 'rent')
    list_filter = ('hall', 'sharing_type')
    search_fields = ('number',)

@admin.register(HallAmenity)
class HallAmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'hall', 'fee')
    list_filter = ('hall',)
    search_fields = ('name',)
