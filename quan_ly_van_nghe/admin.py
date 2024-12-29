from django.contrib import admin
from .models import Location, EventProgram, Task


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')  
    search_fields = ('name', 'address')  


@admin.register(EventProgram)
class EventProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'location', 'status')  
    list_filter = ('status', 'location')  
    search_fields = ('name', 'location__name')  


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'deadline') 
    search_fields = ('name', 'event__name')  
    list_filter = ('deadline',)  
