from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User

class EventCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_address = models.TextField()
    event_location = models.CharField(max_length=200)
    event_date_time = models.DateTimeField()
    event_category = models.ForeignKey('EventCategory', on_delete=models.SET_NULL, null=True)
    total_participants = models.PositiveIntegerField(default=0)
    participants = models.ManyToManyField(User, related_name='events', blank=True)
    event_image = models.ImageField(upload_to='event_images/', null=True, blank=True)

    def __str__(self):
        return self.event_name