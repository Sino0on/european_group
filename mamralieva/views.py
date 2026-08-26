import json
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import gettext_lazy as _
from main.models import (
    CompanyInfo, Statistic, Service, Testimonial,
    EmploymentCountry, UniversityCountry,
    LanguageCourse, VisaType,
    TourDestination, TourDeal,
    LegalService, CompanyPackage,
    Partner, HeroSlide,
)
from .models import BlogPost

_ICON_STROKE = 'stroke="var(--brand-ink)" stroke-width="1.7" fill="none" stroke-linecap="round" stroke-linejoin="round"'

_ICONS = {
    'briefcase': f'<svg width="24" height="24" viewBox="0 0 24 24" {_ICON_STROKE}><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M3 12h18"/></svg>',
    'graduation': f'<svg width="24" height="24" viewBox="0 0 24 24" {_ICON_STROKE}><path d="M22 10 12 5 2 10l10 5 10-5Z"/><path d="M6 12v5c0 1.5 2.5 3 6 3s6-1.5 6-3v-5"/></svg>',
    'passport': f'<svg width="24" height="24" viewBox="0 0 24 24" {_ICON_STROKE}><rect x="5" y="2" width="14" height="20" rx="2"/><circle cx="12" cy="10" r="3"/><path d="M9 17h6"/></svg>',
    'palm': f'<svg width="24" height="24" viewBox="0 0 24 24" {_ICON_STROKE}><path d="M12 22V12"/><path d="M12 12c-3-4-8-3-9-1 2 2 6 2 9 1Z"/><path d="M12 12c3-4 8-3 9-1-2 2-6 2-9 1Z"/><path d="M12 12c-1-4 1-8 3-9-1 3-1 7-3 9Z"/></svg>',
    'scale': f'<svg width="24" height="24" viewBox="0 0 24 24" {_ICON_STROKE}><path d="M12 3v18"/><path d="M5 8h14"/><path d="M5 8 2 15a3 3 0 0 0 6 0L5 8Z"/><path d="M19 8l-3 7a3 3 0 0 0 6 0l-3-7Z"/></svg>',
    'building': f'<svg width="24" height="24" viewBox="0 0 24 24" {_ICON_STROKE}><rect x="4" y="3" width="16" height="18" rx="1"/><path d="M9 8h1M14 8h1M9 12h1M14 12h1M9 16h1M14 16h1"/></svg>',
    'book': f'<svg width="24" height="24" viewBox="0 0 24 24" {_ICON_STROKE}><path d="M4 4h6a2 2 0 0 1 2 2v14a1.5 1.5 0 0 0-2-2H4V4Z"/><path d="M20 4h-6a2 2 0 0 0-2 2v14a1.5 1.5 0 0 1 2-2h6V4Z"/></svg>',
}


def _service_cards():
    return [
        {'title': _('Трудоустройство за рубежом'), 'icon': _ICONS['briefcase'],
         'description': _('Официальные вакансии в Европе: контракты, визовая поддержка, сопровождение на месте.'),
         'url': reverse_lazy('mamralieva:jobs')},
        {'title': _('Образование за рубежом'), 'icon': _ICONS['graduation'],
         'description': _('Подбор университета, помощь с поступлением и подготовкой документов.'),
         'url': reverse_lazy('mamralieva:study')},
        {'title': _('Визовая поддержка'), 'icon': _ICONS['passport'],
         'description': _('Подготовка и подача документов на визу — быстро и без ошибок.'),
         'url': reverse_lazy('mamralieva:visa')},
        {'title': _('Туры'), 'icon': _ICONS['palm'],
         'description': _('Подбор туров и горящих предложений под ваш бюджет и даты.'),
         'url': reverse_lazy('mamralieva:tour')},
        {'title': _('Юридический консалтинг'), 'icon': _ICONS['scale'],
         'description': _('Правовое сопровождение бизнеса и физических лиц в Кыргызстане и за рубежом.'),
         'url': reverse_lazy('mamralieva:law')},
        {'title': _('Регистрация компании'), 'icon': _ICONS['building'],
         'description': _('Полное сопровождение регистрации и запуска бизнеса под ключ.'),
         'url': reverse_lazy('mamralieva:company')},
        {'title': _('Языковые курсы'), 'icon': _ICONS['book'],
         'description': _('Подготовка к языковым экзаменам и обучение с нуля до продвинутого уровня.'),
         'url': reverse_lazy('mamralieva:lang_courses')},
    ]


def _process_steps():
    return [
        {'title': _('Консультация'), 'description': _('Обсуждаем цели, оцениваем шансы и подбираем оптимальный вариант.')},
        {'title': _('Документы'), 'description': _('Готовим и проверяем полный пакет документов вместе с вами.')},
        {'title': _('Подача'), 'description': _('Подаём заявку и сопровождаем на каждом этапе рассмотрения.')},
        {'title': _('Старт'), 'description': _('Помогаем с оформлением на месте — от визы до первого дня.')},
    ]


def _get_base_context():
    return {
        'company': CompanyInfo.get(),
    }


def index(request):
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
                'link': u.link or '',
                'google_maps_link': u.google_maps_link or '',
            }
            for u in uc.universities.filter(is_active=True)
        ]

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
        'service_cards': _service_cards(),
        'process_steps': _process_steps(),
        'blog_posts': BlogPost.objects.filter(is_active=True)[:3],
    })
    return render(request, 'mamralieva/index.html', context)


def company(request):
    context = _get_base_context()
    context.update({
        'packages': CompanyPackage.objects.filter(is_active=True).prefetch_related('features'),
    })
    return render(request, 'mamralieva/company.html', context)


def jobs(request):
    emp_countries = EmploymentCountry.objects.filter(is_active=True).prefetch_related('benefits', 'jobs')
    employment_json = {}
    for ec in emp_countries:
        # один и тот же отфильтрованный список используем и в шаблоне, и в JSON,
        # чтобы индекс вакансии в модалке совпадал с индексом в карточке
        ec.active_jobs = list(ec.jobs.filter(is_active=True))
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
                for j in ec.active_jobs
            ],
        }

    context = _get_base_context()
    context.update({
        'emp_countries': emp_countries,
        # передаём как есть — {{ |json_script }} в шаблоне сам сериализует в JSON
        'employment_json': employment_json,
    })
    return render(request, 'mamralieva/jobs.html', context)


def lang_courses(request):
    context = _get_base_context()
    context.update({
        'language_courses': LanguageCourse.objects.filter(is_active=True),
    })
    return render(request, 'mamralieva/lang_courses.html', context)


def law(request):
    context = _get_base_context()
    context.update({
        'legal_services': LegalService.objects.filter(is_active=True),
    })
    return render(request, 'mamralieva/law.html', context)


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
                'link': u.link or '',
                'google_maps_link': u.google_maps_link or '',
            }
            for u in uc.universities.filter(is_active=True)
        ]

    context = _get_base_context()
    context.update({
        'uni_countries': uni_countries,
        'universities_json': json.dumps(universities_json, cls=DjangoJSONEncoder),
    })
    return render(request, 'mamralieva/study.html', context)


def visa(request):
    context = _get_base_context()
    context.update({
        'visa_types': VisaType.objects.filter(is_active=True),
    })
    return render(request, 'mamralieva/visa.html', context)


def university_detail(request):
    context = _get_base_context()
    return render(request, 'mamralieva/university_detail.html', context)


def tour(request):
    context = _get_base_context()
    context.update({
        'destinations': TourDestination.objects.filter(is_active=True),
        'deals': TourDeal.objects.filter(is_active=True).select_related('destination'),
    })
    return render(request, 'mamralieva/tour.html', context)


def blog(request):
    context = _get_base_context()
    context.update({
        'posts': BlogPost.objects.filter(is_active=True),
    })
    return render(request, 'mamralieva/blog.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_active=True)
    if post.is_external:
        return redirect(post.external_url)
    context = _get_base_context()
    context.update({
        'post': post,
        'other_posts': BlogPost.objects.filter(is_active=True).exclude(pk=post.pk)[:3],
    })
    return render(request, 'mamralieva/blog_detail.html', context)
