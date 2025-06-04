from django.contrib import admin
from .models import Event, EventCategory

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_date_time', 'event_location', 'total_participants', 'event_category')
    list_filter = ('event_date_time', 'event_category')
    search_fields = ('event_name', 'event_location')
    filter_horizontal = ('participants',)  