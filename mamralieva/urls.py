from django.urls import path
from main.views import submit_lead
from .views import *

app_name = 'mamralieva'

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
    path('blog/', blog, name='blog'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path('api/lead/', submit_lead, name='submit_lead'),
]
