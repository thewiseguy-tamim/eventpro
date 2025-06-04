from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
import os
from .models import Event

class EventForm(forms.ModelForm):
    clear_image = forms.BooleanField(required=False, label="Remove existing image")

    class Meta:
        model = Event
        fields = [
            'event_name',
            'event_address',
            'event_location',
            'event_date_time',
            'event_category',
            'event_image'
        ]
        widgets = {
            'event_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'event_category': forms.Select(),
            'event_address': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_event_date_time(self):
        event_date_time = self.cleaned_data.get('event_date_time')
        if event_date_time and event_date_time < timezone.now():
            raise ValidationError("Event date and time cannot be in the past.")
        return event_date_time

    def clean_event_image(self):
        image = self.cleaned_data.get('event_image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError("Image file too large (max 5MB).")
            valid_extensions = ['.jpg', '.jpeg', '.png']
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError("Unsupported file format. Use JPG or PNG.")
        return image

    def clean(self):
        cleaned_data = super().clean()
        clear_image = cleaned_data.get('clear_image')
        event_image = cleaned_data.get('event_image')
        if clear_image and event_image:
            raise ValidationError("Cannot upload a new image and remove the existing one at the same time.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Retrieve original image before update
        original_image = None
        if instance.pk:
            try:
                original_instance = Event.objects.get(pk=instance.pk)
                original_image = original_instance.event_image
            except Event.DoesNotExist:
                pass

        clear_image = self.cleaned_data.get('clear_image')
        new_image = self.cleaned_data.get('event_image')

        # Handle image removal
        if clear_image:
            if original_image:
                original_image.delete(save=False)
            instance.event_image = None

        # Handle new image upload
        elif new_image and new_image != original_image:
            if original_image:
                original_image.delete(save=False)
            instance.event_image = new_image

        if commit:
            instance.save()
            if hasattr(self, 'save_m2m'):
                self.save_m2m()
        return instance
