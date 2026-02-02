from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('company/', company, name='company'),
    path('jobs/', jobs, name='jobs'),
    path('lang_courses/', lang_courses, name='lang_courses'),
    path('law/', law, name='law'),
    path('study/', study, name='study'),
    path('visa/', visa, name='visa'),
    path('university/', university_detail, name='university_detail'),
    path('tour/', tour, name='tour'),
]