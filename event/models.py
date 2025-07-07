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
    
class LandingPageSettings(models.Model):
    hero_image = models.ImageField(upload_to='hero_images/', default='hero_images/default.jpg')
    countdown_date = models.DateTimeField()
    featured_event_1 = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, related_name='featured_1')
    featured_event_2 = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, related_name='featured_2')
    featured_event_3 = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, related_name='featured_3')

    def __str__(self):
        return "Landing Page Settings"