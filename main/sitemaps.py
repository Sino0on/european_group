from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    protocol = 'https'
    i18n = True
    languages = ('ru', 'ky', 'en')
    alternates = True

    pages = [
        ('index',      1.0,  'daily'),
        ('jobs',       0.9,  'weekly'),
        ('study',      0.9,  'weekly'),
        ('visa',       0.9,  'weekly'),
        ('tour',       0.9,  'weekly'),
        ('lang_courses', 0.8, 'weekly'),
        ('law',        0.8,  'weekly'),
        ('company',    0.8,  'weekly'),
    ]

    def items(self):
        return self.pages

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]

    def changefreq(self, item):
        return item[2]
