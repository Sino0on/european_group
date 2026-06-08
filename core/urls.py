from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from main.sitemaps import StaticViewSitemap

sitemaps = {'static': StaticViewSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain',
        extra_context={'site_url': settings.SITE_URL},
    )),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('', include('main.urls')),
)