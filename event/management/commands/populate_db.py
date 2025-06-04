from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from event.models import EventCategory, Event

class Command(BaseCommand):
    help = 'Populates the database with sample events and categories'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Event.objects.all().delete()
        EventCategory.objects.all().delete()

        # Create event categories
        categories = [
            'Music', 'Sports', 'Tech', 'Art', 'Food', 'Networking', 'Education'
        ]
        category_objects = []
        for name in categories:
            category, _ = EventCategory.objects.get_or_create(name=name)
            category_objects.append(category)

        # Sample event data
        event_data = [
            {
                'name': 'Summer Music Festival',
                'address': '123 Central Park, NY',
                'location': 'New York, NY',
                'category': 'Music',
                'participants': 150
            },
            {
                'name': 'Tech Conference 2025',
                'address': '456 Tech Hub, SF',
                'location': 'San Francisco, CA',
                'category': 'Tech',
                'participants': 300
            },
            {
                'name': 'Marathon City Run',
                'address': '789 Downtown, Chicago',
                'location': 'Chicago, IL',
                'category': 'Sports',
                'participants': 500
            },
            {
                'name': 'Art Gallery Opening',
                'address': '101 Art Street, Miami',
                'location': 'Miami, FL',
                'category': 'Art',
                'participants': 80
            },
            {
                'name': 'Food Truck Festival',
                'address': '202 Food Plaza, Austin',
                'location': 'Austin, TX',
                'category': 'Food',
                'participants': 200
            },
        ]

        # Create events
        for event in event_data:
            category = EventCategory.objects.get(name=event['category'])
            Event.objects.create(
                event_name=event['name'],
                event_address=event['address'],
                event_location=event['location'],
                event_date_time=timezone.now() + timedelta(days=random.randint(1, 30)),
                event_category=category,
                total_participants=event['participants'],
            )

        self.stdout.write(self.style.SUCCESS(f"Created {len(categories)} categories and {len(event_data)} events."))