# event/urls.py
from django.urls import path
from .views import (
    EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView,
    RSVPView, AdminDashboardView, ManagerDashboardView, ClientDashboardView, HomeView,
    UserRoleUpdateView, UserStatusToggleView, EventCategoryCreateView, EventCategoryDeleteView,
    CancelRegistrationView, AboutView, contact_view
    
)

urlpatterns = [
    # Public views
    path('', EventListView.as_view(), name='event_list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('<int:pk>/rsvp/', RSVPView.as_view(), name='event_rsvp'),
    path('add-category/', EventCategoryCreateView.as_view(), name='eventcategory-add'),
    # path('category/<int:pk>/edit/', EventCategoryUpdateView.as_view(), name='eventcategory-edit'),
    path('category/<int:pk>/delete/', EventCategoryDeleteView.as_view(), name='eventcategory-delete'),
    path('cancel/<int:event_id>/', CancelRegistrationView.as_view(), name='cancel_registration'),
    
    # Admin/Manager views
    path('create/', EventCreateView.as_view(), name='event_create'),
    path('<int:pk>/edit/', EventUpdateView.as_view(), name='event_update'),
    path('<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
    
    # Dashboard views
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/manager/', ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('dashboard/client/', ClientDashboardView.as_view(), name='client_dashboard'),

    path('users/<int:pk>/role/', UserRoleUpdateView.as_view(), name='user_role_update'),
    path('users/<int:pk>/status/', UserStatusToggleView.as_view(), name='user_status_toggle'),

    path('about/', AboutView.as_view(), name='about'),
    path('contact/', contact_view, name='contact'),
    
    
]

