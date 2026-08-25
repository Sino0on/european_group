from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class MamralievaSitemap(Sitemap):
    protocol = 'https'
    i18n = True
    languages = ('ru', 'ky', 'en')
    alternates = True

    pages = [
        ('mamralieva:index', 1.0, 'daily'),
        ('mamralieva:jobs', 0.9, 'weekly'),
        ('mamralieva:study', 0.9, 'weekly'),
        ('mamralieva:visa', 0.9, 'weekly'),
        ('mamralieva:tour', 0.9, 'weekly'),
        ('mamralieva:lang_courses', 0.8, 'weekly'),
        ('mamralieva:law', 0.8, 'weekly'),
        ('mamralieva:company', 0.8, 'weekly'),
    ]

    def items(self):
        return self.pages

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]

    def changefreq(self, item):
        return item[2]
