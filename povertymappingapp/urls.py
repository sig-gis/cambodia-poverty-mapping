from __future__ import absolute_import, print_function, unicode_literals
from cms.sitemaps import CMSSitemap
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.conf.urls.i18n import i18n_patterns
from django.views.static import serve
from django.views.generic import TemplateView
from mapclient import api as mapclient_api

from django.conf import settings
from .views import switch_language  # Import the custom view

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/mapclient/', mapclient_api.api),
    path('switch_language/', switch_language, name='switch_language'),  # Add this line
]

urlpatterns += i18n_patterns(
    path('', TemplateView.as_view(template_name="home.html")),
    path('map/', TemplateView.as_view(template_name="map.html")),
    path('home/', TemplateView.as_view(template_name="home.html")),
    path('method/', TemplateView.as_view(template_name="method.html")),
    path('about/', TemplateView.as_view(template_name="about.html")),
    path('i18n/', include('django.conf.urls.i18n')),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
