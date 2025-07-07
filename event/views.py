from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django import forms
from django.utils import timezone
from django.db import models
import json
from .models import Event, EventCategory
from users.models import User
from django.utils.dateparse import parse_datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
import logging
from django.db import models
from django.utils import timezone
from .forms import EventForm
from django.contrib.messages.views import SuccessMessageMixin


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Count, Sum, Q
import json
from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Count, Sum, Q
from django.shortcuts import redirect
from .models import Event, EventCategory, LandingPageSettings
import json
from datetime import datetime, timedelta

class RoleRequiredMixin:
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role not in self.allowed_roles:
            messages.error(request, "You don't have permission to access this page.")
            return redirect('client_dashboard')
        return super().dispatch(request, *args, **kwargs)

class AboutView(TemplateView):
    template_name = 'about.html'


from django.core.mail import send_mail
from django.conf import settings

class CancelRegistrationView(LoginRequiredMixin, View):
    def post(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        if request.user in event.participants.all():
            event.participants.remove(request.user)
            event.total_participants -= 1
            event.save()
            send_mail(
                'Cancellation Confirmation',
                f'You have successfully cancelled your registration for {event.event_name}.',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=True,
            )
            messages.success(request, f"Registration for {event.event_name} cancelled successfully.")
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'error': 'You are not registered for this event.'}, status=400)

class EventCategoryCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = EventCategory
    fields = ['name']
    template_name = 'event/eventcategory_form.html'
    allowed_roles = ['admin', 'manager']

    def form_valid(self, form):
        messages.success(self.request, "Category created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to create category. Please check the form.")
        return super().form_invalid(form)

    def get_success_url(self):
        # Redirect based on user role
        if self.request.user.role == 'admin':
            return reverse_lazy('admin_dashboard') + '?tab=categories'
        return reverse_lazy('manager_dashboard') + '?tab=categories'

class EventCategoryDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = EventCategory
    template_name = 'event/eventcategory_confirm_delete.html'
    allowed_roles = ['admin', 'manager']

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        category_name = category.name
        
        if category.event_set.exists():
            messages.error(request, f"Cannot delete category '{category_name}' because it has {category.event_set.count()} associated events.")
            return redirect(self.get_success_url())
        
        messages.success(request, f"Category '{category_name}' deleted successfully!")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        # Redirect based on user role
        if self.request.user.role == 'admin':
            return reverse_lazy('admin_dashboard') + '?tab=categories'
        return reverse_lazy('manager_dashboard') + '?tab=categories'



class EventListView(ListView):
    model = Event
    template_name = 'event/event_list.html'
    context_object_name = 'events'


class EventDetailView(DetailView):
    model = Event
    template_name = 'event/event_detail.html'


class EventCreateView(LoginRequiredMixin, RoleRequiredMixin, SuccessMessageMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event/event_form.html'
    success_url = reverse_lazy('admin_dashboard')
    allowed_roles = ['admin', 'manager']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = EventCategory.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Event created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to create event. Please check the form.")
        return super().form_invalid(form)


class EventUpdateView(LoginRequiredMixin, RoleRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event/event_form.html'
    success_url = reverse_lazy('admin_dashboard')
    allowed_roles = ['admin', 'manager']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = EventCategory.objects.all()
        context['object'] = self.get_object()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Event updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to update event. Please check the form.")
        return super().form_invalid(form)


class EventDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Event
    template_name = 'event/event_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard')
    allowed_roles = ['admin', 'manager']


class RSVPView(LoginRequiredMixin, DetailView):
    model = Event

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        if request.user in event.participants.all():
            messages.warning(request, "You have already RSVPed to this event.")
        else:
            event.participants.add(request.user)
            event.total_participants += 1
            event.save()
            send_mail(
                'RSVP Confirmation',
                f'You have successfully RSVPed to {event.event_name}.',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
            messages.success(request, f'You have RSVPed to {event.event_name}!')
        return redirect('event_detail', pk=event.pk)

class UserRoleUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = User
    fields = ['role']
    template_name = 'dashboard/user_role_form.html'
    success_url = reverse_lazy('admin_dashboard')
    allowed_roles = ['admin']

    def form_valid(self, form):
        messages.success(self.request, "User role updated successfully!")
        return super().form_valid(form)


class UserStatusToggleView(LoginRequiredMixin, RoleRequiredMixin, View):
    allowed_roles = ['admin']

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_active = not user.is_active
        user.save()
        status = 'activated' if user.is_active else 'deactivated'
        messages.success(request, f"User {status} successfully!")
        return redirect('admin_dashboard')

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/admin_dashboard.html'
    allowed_roles = ['admin']

    def post(self, request, *args, **kwargs):
        settings, created = LandingPageSettings.objects.get_or_create(pk=1)
        if 'hero_image' in request.FILES:
            settings.hero_image = request.FILES['hero_image']
        countdown_date = request.POST.get('countdown_date')
        if countdown_date:
            settings.countdown_date = timezone.datetime.strptime(countdown_date, '%Y-%m-%dT%H:%M')
        settings.featured_event_1 = Event.objects.filter(id=request.POST.get('featured_event_1')).first()
        settings.featured_event_2 = Event.objects.filter(id=request.POST.get('featured_event_2')).first()
        settings.featured_event_3 = Event.objects.filter(id=request.POST.get('featured_event_3')).first()
        settings.save()
        return redirect('admin_dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_status = self.request.GET.get('event_status', '')
        search_query = self.request.GET.get('search', '')
        role_filter = self.request.GET.get('role', '')
        status_filter = self.request.GET.get('status', '')

        # Events
        events = Event.objects.all().order_by('-event_date_time')
        if event_status:
            now = timezone.now()
            if event_status == 'upcoming':
                events = events.filter(event_date_time__gte=now)
            elif event_status == 'past':
                events = events.filter(event_date_time__lt=now)
        if search_query:
            events = events.filter(
                Q(event_name__icontains=search_query) |
                Q(event_location__icontains=search_query)
            )

        # Users
        users = User.objects.all().order_by('-date_joined')
        if role_filter:
            users = users.filter(role=role_filter)
        if status_filter:
            users = users.filter(is_active=(status_filter == 'active'))
        if search_query:
            users = users.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )

        # Basic stats
        total_events = Event.objects.count()
        total_users = User.objects.count()
        active_events = Event.objects.filter(event_date_time__gte=timezone.now()).count()
        total_rsvps = Event.objects.aggregate(total=Sum('total_participants'))['total'] or 0

        # Landing page settings
        settings, created = LandingPageSettings.objects.get_or_create(
            pk=1,
            defaults={'countdown_date': timezone.now() + timedelta(days=30)}
        )
        all_events = Event.objects.all().order_by('event_date_time')

        # Chart data preparation
        chart_data = self.get_chart_data()

        context.update({
            'events': events,
            'users': users,
            'categories': EventCategory.objects.all(),
            'total_events': total_events,
            'total_users': total_users,
            'active_events': active_events,
            'total_rsvps': total_rsvps,
            'event_status': event_status,
            'search_query': search_query,
            'role_filter': role_filter,
            'status_filter': status_filter,
            'chart_data': chart_data,
            'landing_settings': settings,
            'all_events': all_events,
        })
        return context

    def get_chart_data(self):
        today = timezone.now().date()
        week_days = []
        events_count = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            week_days.append(day.strftime('%a'))
            count = Event.objects.filter(event_date_time__date=day).count()
            events_count.append(count)
        if not week_days:
            week_days = [datetime.now().strftime('%a')]
            events_count = [0]

        role_data = User.objects.values('role').annotate(count=Count('id')).order_by('-count')
        role_labels = [item['role'].title() for item in role_data]
        role_counts = [item['count'] for item in role_data]
        if not role_labels:
            role_labels = ['Admin', 'Manager', 'Client']
            role_counts = [0, 0, 0]

        six_months_ago = today - timedelta(days=180)
        monthly_events_data = []
        month_labels = []
        for i in range(5, -1, -1):
            month_start = (today - timedelta(days=30 * i)).replace(day=1)
            count = Event.objects.filter(
                event_date_time__year=month_start.year,
                event_date_time__month=month_start.month
            ).count()
            monthly_events_data.append(count)
            month_labels.append(month_start.strftime('%b'))
        if not month_labels:
            month_labels = [datetime.now().strftime('%b')]
            monthly_events_data = [0]

        total_rsvps = Event.objects.aggregate(total=Sum('total_participants'))['total'] or 0
        total_events = Event.objects.count()
        max_capacity = total_events * 50
        available_spots = max(0, max_capacity - total_rsvps)

        return {
            'weekly_activity': {
                'labels': json.dumps(week_days),
                'data': json.dumps(events_count),
            },
            'user_roles': {
                'labels': json.dumps(role_labels),
                'data': json.dumps(role_counts),
            },
            'monthly_events': {
                'labels': json.dumps(month_labels),
                'data': json.dumps(monthly_events_data),
            },
            'rsvp_data': {
                'labels': json.dumps(['Confirmed RSVPs', 'Available Spots']),
                'data': json.dumps([total_rsvps, available_spots]),
            }
        }





class ManagerDashboardView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = 'dashboard/manager_dashboard.html'
    allowed_roles = ['manager']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = Event.objects.all().order_by('-event_date_time')
        event_status = self.request.GET.get('event_status', '')
        search_query = self.request.GET.get('search', '')

        if event_status:
            now = timezone.now()
            if event_status == 'upcoming':
                events = events.filter(event_date_time__gte=now)
            elif event_status == 'past':
                events = events.filter(event_date_time__lt=now)
        if search_query:
            events = events.filter(
                models.Q(event_name__icontains=search_query) |
                models.Q(event_location__icontains=search_query) |
                models.Q(event_category__name__icontains=search_query)
            )

        context['events'] = events
        context['categories'] = EventCategory.objects.all()
        context['total_events'] = Event.objects.count()
        context['total_users'] = User.objects.count()  # Added
        context['active_events'] = Event.objects.filter(event_date_time__gte=timezone.now()).count()
        context['total_rsvps'] = Event.objects.aggregate(
            total=models.Sum('total_participants')
        )['total'] or 0  # Renamed from total_participants to total_rsvps
        context['event_status'] = event_status
        context['search_query'] = search_query
        return context

class ClientDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/client_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_events = Event.objects.filter(participants=self.request.user).select_related('event_category').order_by('-event_date_time')
        search_query = self.request.GET.get('search', '')

        if search_query:
            my_events = my_events.filter(
                Q(event_name__icontains=search_query) |
                Q(event_location__icontains=search_query) |
                Q(event_category__name__icontains=search_query)
            )

        context['my_events'] = my_events
        context['total_registered_events'] = my_events.count()
        context['upcoming_events'] = my_events.filter(event_date_time__gte=timezone.now()).count()
        context['past_events'] = my_events.filter(event_date_time__lt=timezone.now()).count()
        context['search_query'] = search_query
        context['current_time'] = timezone.now()
        return context


class HomeView(ListView):
    model = Event
    template_name = 'home.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settings, created = LandingPageSettings.objects.get_or_create(
            pk=1,
            defaults={'countdown_date': timezone.now() + timedelta(days=30)}
        )
        context['landing_settings'] = settings
        context['landing_settings'].featured_events = [
            settings.featured_event_1,
            settings.featured_event_2,
            settings.featured_event_3
        ]
        context['landing_settings'].featured_events = [e for e in context['landing_settings'].featured_events if e]
        return context
    
logger = logging.getLogger(__name__)

def contact_view(request):
    """
    Handle contact form submissions and display the contact page
    """
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            event_type = request.POST.get('event_type', '').strip()
            guest_count = request.POST.get('guest_count', '').strip()
            event_date = request.POST.get('event_date', '').strip()
            message = request.POST.get('message', '').strip()
            
            # Basic validation
            if not all([first_name, last_name, email, event_type, message]):
                messages.error(request, 'Please fill in all required fields.')
                return render(request, 'contact.html')
            
            # Format email content
            email_subject = f"New Event Inquiry - {event_type.title()}"
            email_body = f"""
New event inquiry received from EventPro website:

Contact Information:
- Name: {first_name} {last_name}
- Email: {email}
- Phone: {phone if phone else 'Not provided'}

Event Details:
- Event Type: {event_type.title()}
- Expected Guests: {guest_count if guest_count else 'Not specified'}
- Event Date: {event_date if event_date else 'Not specified'}

Message:
{message}

---
This inquiry was submitted through the EventPro contact form.
            """
            
            # Send email notification (you can customize the recipient)
            try:
                send_mail(
                    subject=email_subject,
                    message=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL if hasattr(settings, 'CONTACT_EMAIL') else 'info@eventpro.com'],
                    fail_silently=False,
                )
                
                # Send confirmation email to the user
                confirmation_subject = "Thank you for contacting EventPro!"
                confirmation_body = f"""
Dear {first_name},

Thank you for reaching out to EventPro! We've received your inquiry about your {event_type} event and are excited to help bring your vision to life.

Here's a summary of your inquiry:
- Event Type: {event_type.title()}
- Expected Guests: {guest_count if guest_count else 'Not specified'}
- Event Date: {event_date if event_date else 'Not specified'}

One of our event specialists will review your requirements and get back to you within 24 hours. In the meantime, feel free to explore our portfolio and services on our website.

If you have any urgent questions, don't hesitate to call us at +1 (555) 123-4567.

Best regards,
The EventPro Team

---
EventPro - Creating Unforgettable Experiences
123 Event Street, City Center, NY 10001
Phone: +1 (555) 123-4567
Email: info@eventpro.com
Website: www.eventpro.com
                """
                
                send_mail(
                    subject=confirmation_subject,
                    message=confirmation_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,  # Don't fail if confirmation email fails
                )
                
            except Exception as email_error:
                logger.error(f"Error sending contact form email: {email_error}")
                # Still show success to user even if email fails
                pass
            
            messages.success(
                request, 
                f'Thank you {first_name}! Your message has been sent successfully. '
                'We\'ll get back to you within 24 hours.'
            )
            
            # Redirect to prevent form resubmission
            return redirect('contact')
            
        except Exception as e:
            logger.error(f"Error processing contact form: {e}")
            messages.error(
                request, 
                'Sorry, there was an error sending your message. Please try again or contact us directly.'
            )
            return render(request, 'contact.html')
    
    # GET request - display the contact form
    return render(request, 'contact.html')


# Alternative model-based approach (optional)
# If you want to store contact inquiries in the database

from django.db import models
from django.utils import timezone

class ContactInquiry(models.Model):
    """
    Model to store contact form submissions
    """
    EVENT_TYPE_CHOICES = [
        ('wedding', 'Wedding'),
        ('corporate', 'Corporate Event'),
        ('conference', 'Conference'),
        ('party', 'Private Party'),
        ('fundraiser', 'Fundraiser'),
        ('other', 'Other'),
    ]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    guest_count = models.PositiveIntegerField(null=True, blank=True)
    event_date = models.DateField(null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_responded = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Inquiry'
        verbose_name_plural = 'Contact Inquiries'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.event_type}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


def contact_view_with_model(request):
    """
    Alternative contact view that saves inquiries to database
    """
    if request.method == 'POST':
        try:
            # Create inquiry object
            inquiry = ContactInquiry(
                first_name=request.POST.get('first_name', '').strip(),
                last_name=request.POST.get('last_name', '').strip(),
                email=request.POST.get('email', '').strip(),
                phone=request.POST.get('phone', '').strip(),
                event_type=request.POST.get('event_type', '').strip(),
                guest_count=int(request.POST.get('guest_count')) if request.POST.get('guest_count') else None,
                event_date=request.POST.get('event_date') or None,
                message=request.POST.get('message', '').strip(),
            )
            
            # Validate required fields
            if not all([inquiry.first_name, inquiry.last_name, inquiry.email, inquiry.event_type, inquiry.message]):
                messages.error(request, 'Please fill in all required fields.')
                return render(request, 'contact.html')
            
            # Save to database
            inquiry.save()
            
            # Send email notification (same as above)
            # ... email sending code ...
            
            messages.success(
                request, 
                f'Thank you {inquiry.first_name}! Your inquiry has been saved and we\'ll contact you soon.'
            )
            
            return redirect('contact')
            
        except Exception as e:
            logger.error(f"Error saving contact inquiry: {e}")
            messages.error(request, 'There was an error processing your request. Please try again.')
            return render(request, 'contact.html')
    
    return render(request, 'contact.html')