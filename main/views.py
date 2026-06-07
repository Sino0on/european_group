import json
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from .models import (
    CompanyInfo, Statistic, Service, Testimonial,
    EmploymentCountry, UniversityCountry,
    LanguageCourse, VisaType,
    TourDestination, TourDeal,
    LegalService, CompanyPackage,
    Partner,
)


def _get_base_context():
    return {
        'company': CompanyInfo.get(),
    }


def index(request):
    # Университеты: строим JSON для JS-виджета
    uni_countries = UniversityCountry.objects.filter(is_active=True).prefetch_related('universities')
    universities_json = {}
    for uc in uni_countries:
        universities_json[uc.slug] = [
            {
                'id': u.slug,
                'name': u.name,
                'location': u.location,
                'img': u.image.url if u.image else '',
                'desc': u.description,
            }
            for u in uc.universities.filter(is_active=True)
        ]

    # Трудоустройство: строим JSON для JS-виджета
    emp_countries = EmploymentCountry.objects.filter(is_active=True).prefetch_related('benefits', 'jobs')
    employment_json = {}
    for ec in emp_countries:
        employment_json[ec.slug] = {
            'title': ec.name,
            'desc': ec.description,
            'benefits': [b.text for b in ec.benefits.all()],
            'jobs': [{'role': j.role, 'salary': j.salary} for j in ec.jobs.all()],
        }

    context = _get_base_context()
    context.update({
        'statistics': Statistic.objects.filter(is_active=True),
        'services': Service.objects.filter(is_active=True),
        'testimonials': Testimonial.objects.filter(is_active=True),
        'uni_countries': uni_countries,
        'universities_json': json.dumps(universities_json, cls=DjangoJSONEncoder),
        'emp_countries': emp_countries,
        'employment_json': json.dumps(employment_json, cls=DjangoJSONEncoder),
        'language_courses': LanguageCourse.objects.filter(is_active=True),
        'partners': Partner.objects.filter(is_active=True),
    })
    return render(request, 'index.html', context)


def company(request):
    context = _get_base_context()
    context.update({
        'packages': CompanyPackage.objects.filter(is_active=True).prefetch_related('features'),
    })
    return render(request, 'company.html', context)


def jobs(request):
    emp_countries = EmploymentCountry.objects.filter(is_active=True).prefetch_related('benefits', 'jobs')
    employment_json = {}
    for ec in emp_countries:
        employment_json[ec.slug] = {
            'title': ec.name,
            'desc': ec.description,
            'benefits': [b.text for b in ec.benefits.all()],
            'jobs': [{'role': j.role, 'salary': j.salary} for j in ec.jobs.all()],
        }

    context = _get_base_context()
    context.update({
        'emp_countries': emp_countries,
        'employment_json': json.dumps(employment_json, cls=DjangoJSONEncoder),
    })
    return render(request, 'jobs.html', context)


def lang_courses(request):
    context = _get_base_context()
    context.update({
        'language_courses': LanguageCourse.objects.filter(is_active=True),
    })
    return render(request, 'lang_courses.html', context)


def law(request):
    context = _get_base_context()
    context.update({
        'legal_services': LegalService.objects.filter(is_active=True),
    })
    return render(request, 'law.html', context)


def study(request):
    uni_countries = UniversityCountry.objects.filter(is_active=True).prefetch_related('universities')
    universities_json = {}
    for uc in uni_countries:
        universities_json[uc.slug] = [
            {
                'id': u.slug,
                'name': u.name,
                'location': u.location,
                'img': u.image.url if u.image else '',
                'desc': u.description,
            }
            for u in uc.universities.filter(is_active=True)
        ]

    context = _get_base_context()
    context.update({
        'uni_countries': uni_countries,
        'universities_json': json.dumps(universities_json, cls=DjangoJSONEncoder),
    })
    return render(request, 'study.html', context)


def visa(request):
    context = _get_base_context()
    context.update({
        'visa_types': VisaType.objects.filter(is_active=True),
    })
    return render(request, 'visa.html', context)


def university_detail(request):
    context = _get_base_context()
    return render(request, 'university_detail.html', context)


def tour(request):
    context = _get_base_context()
    context.update({
        'destinations': TourDestination.objects.filter(is_active=True),
        'deals': TourDeal.objects.filter(is_active=True).select_related('destination'),
    })
    return render(request, 'tour.html', context)
