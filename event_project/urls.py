from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from event.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('events/', include('event.urls')),
    path('accounts/', include('users.urls')),
]

if settings.DEBUG:
    # Local dev: serve actual media folder
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Prod (Vercel): redirect /media/* to /static/media/* (bundled by collectstatic)
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', RedirectView.as_view(
            url='/static/media/%(path)s', permanent=True
        )),
    ]