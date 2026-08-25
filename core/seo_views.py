from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.template.loader import render_to_string
from main.sitemaps import StaticViewSitemap
from mamralieva.sitemaps import MamralievaSitemap


def _is_new_site(request):
    return 'mamralieva' in request.get_host().lower()


def dynamic_sitemap(request, *args, **kwargs):
    sitemaps = {'static': MamralievaSitemap if _is_new_site(request) else StaticViewSitemap}
    return sitemap(request, sitemaps=sitemaps)


def dynamic_robots(request):
    site_url = f'{request.scheme}://{request.get_host()}'
    content = render_to_string('robots.txt', {'site_url': site_url})
    return HttpResponse(content, content_type='text/plain')
