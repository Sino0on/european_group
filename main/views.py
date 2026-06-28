import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.serializers.json import DjangoJSONEncoder
from .telegram import send_telegram
from .models import (
    CompanyInfo, Statistic, Service, Testimonial,
    EmploymentCountry, UniversityCountry,
    LanguageCourse, VisaType,
    TourDestination, TourDeal,
    LegalService, CompanyPackage,
    Partner, HeroSlide,
)


# Человекочитаемые названия источников заявок
_SOURCE_LABELS = {
    'consultation': '📋 Консультация (главная)',
    'jobs': '💼 Трудоустройство',
    'study': '🎓 Образование за рубежом',
    'visa': '🛂 Визовая поддержка',
    'tour': '✈️ Подбор тура',
    'lang': '🗣 Языковые курсы',
    'law': '⚖️ Юридическая консультация',
    'company': '🏢 Регистрация компании',
    'modal': '💬 Быстрая консультация (модал)',
}

# Человекочитаемые названия полей
_FIELD_LABELS = {
    'name': 'Имя',
    'phone': 'Телефон',
    'whatsapp': 'WhatsApp',
    'country': 'Страна',
    'destination': 'Направление',
    'budget': 'Бюджет',
    'course': 'Курс',
    'service': 'Услуга',
    'program': 'Программа',
    'company_type': 'Тип компании',
    'experience': 'Опыт',
    'message': 'Комментарий',
}


@require_POST
def submit_lead(request):
    try:
        data = json.loads(request.body)
    except (ValueError, TypeError):
        data = request.POST.dict()

    source = data.get('source', 'unknown')
    source_label = _SOURCE_LABELS.get(source, f'📩 Заявка ({source})')

    lines = [f'<b>{source_label}</b>', '']
    for key, label in _FIELD_LABELS.items():
        value = (data.get(key) or '').strip()
        if value:
            lines.append(f'<b>{label}:</b> {value}')

    # Любые дополнительные поля, не вошедшие в _FIELD_LABELS
    known = set(_FIELD_LABELS) | {'source'}
    for key, value in data.items():
        if key not in known and value and str(value).strip():
            lines.append(f'<b>{key}:</b> {value}')

    text = '\n'.join(lines)
    ok = send_telegram(text)
    return JsonResponse({'ok': ok})


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
            'jobs': [
                {
                    'role': j.role,
                    'salary': j.salary,
                    'description': j.description or '',
                    'requirements': j.requirements or '',
                    'duties': j.duties or '',
                    'conditions': j.conditions or '',
                    'image': j.image.url if j.image else '',
                }
                for j in ec.jobs.filter(is_active=True)
            ],
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
        'hero_slides': HeroSlide.objects.filter(is_active=True),
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
            'jobs': [
                {
                    'role': j.role,
                    'salary': j.salary,
                    'description': j.description or '',
                    'requirements': j.requirements or '',
                    'duties': j.duties or '',
                    'conditions': j.conditions or '',
                    'image': j.image.url if j.image else '',
                }
                for j in ec.jobs.filter(is_active=True)
            ],
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
