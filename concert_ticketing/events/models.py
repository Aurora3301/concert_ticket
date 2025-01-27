# events/models.py (correct version)
from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=200)          # Event Name
    date = models.DateTimeField()                    # Date
    venue = models.CharField(max_length=200)         # Venue
    description = models.TextField(blank=True)       # Description
    
    def __str__(self):
        return self.name

class Ticket(models.Model):
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE,
        related_name='tickets'  # Critical for `event.tickets.all()`
    )
    ticket_type = models.CharField(max_length=100)    # Ticket Type
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price
    quantity_available = models.IntegerField()        # Quantity
    
    def __str__(self):
        return f"{self.ticket_type} (${self.price})"