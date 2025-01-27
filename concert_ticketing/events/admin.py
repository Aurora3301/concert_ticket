# events/admin.py
from django.contrib import admin
from .models import Event, Ticket

#admin.site.register(Event)
#admin.site.register(Ticket)

class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0  # Don't show empty slots

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'venue']
    search_fields = ['name', 'venue']
    inlines = [TicketInline]

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['event', 'ticket_type', 'price', 'quantity_available']
    list_filter = ['event', 'ticket_type']