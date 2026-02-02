from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

def company(request):
    return render(request, 'company.html')

def jobs(request):
    return render(request, 'jobs.html')

def lang_courses(request):
    return render(request, 'lang_courses.html')

def law(request):
    return render(request, 'law.html')

def study(request):
    return render(request, 'study.html')

def visa(request):
    return render(request, 'visa.html')

def university_detail(request):
    return render(request, 'university_detail.html')

def tour(request):
    return render(request, 'tour.html')
