from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from event.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('events/', include('event.urls')),
    path('accounts/', include('users.urls')),
]

# Serve media files always (so your hardcoded /media/... works even if DEBUG=False)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)