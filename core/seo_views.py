from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.template.loader import render_to_string
from main.sitemaps import StaticViewSitemap
from mamralieva.sitemaps import MamralievaSitemap, MamralievaBlogSitemap


def _is_new_site(request):
    return 'mamralieva' in request.get_host().lower()


def dynamic_sitemap(request, *args, **kwargs):
    if _is_new_site(request):
        sitemaps = {'static': MamralievaSitemap, 'blog': MamralievaBlogSitemap}
    else:
        sitemaps = {'static': StaticViewSitemap}
    return sitemap(request, sitemaps=sitemaps)


def dynamic_robots(request):
    site_url = f'{request.scheme}://{request.get_host()}'
    content = render_to_string('robots.txt', {'site_url': site_url})
    return HttpResponse(content, content_type='text/plain')
