from django.db import models
from django.utils.timezone import now

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateTimeField(default=now)
    available_tickets = models.PositiveIntegerField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
