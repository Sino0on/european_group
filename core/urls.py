from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from .seo_views import dynamic_sitemap, dynamic_robots

urlpatterns = [
    path("admin/", admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    # sitemap.xml и robots.txt зависят от домена (european-group.kg -> старый
    # сайт, mamralieva.kg -> новый), поэтому раздаём их динамически по Host
    path('sitemap.xml', dynamic_sitemap, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', dynamic_robots),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    # старый сайт (European Group) — теперь живёт под /old/
    path('old/', include('main.urls')),
    # новый сайт (Mamralieva Consulting) — теперь на корне
    path('', include('mamralieva.urls')),
)