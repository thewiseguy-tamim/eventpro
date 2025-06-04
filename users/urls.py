from django.urls import path
from .views import SignUpView, CustomLoginView, ProfileView, MyEventsView, activate_account
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='event_list'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('my-events/', MyEventsView.as_view(), name='my_events'),
    path('activate/<int:uid>/<str:token>/', activate_account, name='activate_account'),
]