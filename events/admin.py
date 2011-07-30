from django.contrib import admin
from events.models import *

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('The basics', {
            'fields': ('title', 'event_datetime', ('type', 'candidate'), 'description'),
        }),
        ('Location information', {
            'fields': ('address', 'city', 'state'),
        }),
        ('Coverage information', {
            'fields': ('covered', 'assigned_to'),
        }),  
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('slug', 'lat', 'lng')
        }),
    )
    search_fields = ['title', 'description']
    list_filter = ['event_datetime', 'type']
    list_display = ('title', 'type', 'event_datetime', 'city', 'state', 'created_date', 'updated_date')
    
admin.site.register(Event, EventAdmin)


class TypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    
admin.site.register(Type, TypeAdmin)