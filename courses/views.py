from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import EnrollForm
import json
from django.urls import reverse

# Данные
COURSES = [
    {
        'title': 'Введение в Python',
        'slug': 'python-intro',
        'short': 'Основы Python: переменные, условия, функции.',
        'teacher': 'Алексей Иванов',
        'duration': '4 недели',
    },
    {
        'title': 'Веб-разработка на Django',
        'slug': 'django-web',
        'short': 'Создание сайтов с Django — от моделей до деплоя.',
        'teacher': 'Мария Петрова',
        'duration': '6 недель',
    },
    {
        'title': 'Машинное обучение — старт',
        'slug': 'ml-start',
        'short': 'Введение в ML: sklearn, базовые алгоритмы.',
        'teacher': 'Екатерина Смирнова',
        'duration': '5 недель',
    },
]

#  найти курс по slug
def get_course(slug):
    for c in COURSES:
        if c['slug'] == slug:
            return c
    return None

# главная страница: список курсов
def index(request):
    # получаем настройки из cookies
    theme = request.COOKIES.get('theme', 'light')
    lang = request.COOKIES.get('lang', 'en')

    # обновляем cookie "last_visited" — добавляем 'index' в начало списка
    last = request.COOKIES.get('last_visited')
    if last:
        try:
            last_list = json.loads(last)
        except Exception:
            last_list = []
    else:
        last_list = []

    # добавляем маркер страницы 'index' (можно хранить slug'и страниц)
    if 'index' in last_list:
        last_list.remove('index')
    last_list.insert(0, 'index')
    # оставим только до 5 последних
    last_list = last_list[:5]

    context = {
        'courses': COURSES,
        'theme': theme,
        'lang': lang,
        'last_visited': last_list,
    }
    response = render(request, 'courses/index.html', context)
    # записываем cookie last_visited (строка JSON)
    response.set_cookie('last_visited', json.dumps(last_list), max_age=30*24*60*60) # 30 дней
    return response

# --- Страница курса
def course_detail(request, slug):
    course = get_course(slug)
    if not course:
        return render(request, 'courses/course_detail.html', {'error': 'Курс не найден'})

    theme = request.COOKIES.get('theme', 'light')
    lang = request.COOKIES.get('lang', 'en')

    # Обновление last_visited: добавляем slug
    last = request.COOKIES.get('last_visited')
    try:
        last_list = json.loads(last) if last else []
    except Exception:
        last_list = []
    if slug in last_list:
        last_list.remove(slug)
    last_list.insert(0, slug)
    last_list = last_list[:5]

    context = {
        'course': course,
        'theme': theme,
        'lang': lang,
        'last_visited': last_list,
        'form': EnrollForm(initial={'course': slug}),
    }

    response = render(request, 'courses/course_detail.html', context)
    response.set_cookie('last_visited', json.dumps(last_list), max_age=30*24*60*60)
    return response

# Обработка формы записи (enroll)
def enroll(request):
    if request.method == 'POST':
        form = EnrollForm(request.POST)
        if form.is_valid():
            #  имитируем успешную запись.
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            course_slug = form.cleaned_data['course']
            # можно вывести сообщение или перенаправить на страницу успеха
            response = render(request, 'courses/index.html', {
                'courses': COURSES,
                'message': f'Спасибо, {name}! Ваша заявка на курс отправлена (эл. почта: {email}).',
                'theme': request.COOKIES.get('theme', 'light'),
                'lang': request.COOKIES.get('lang', 'en'),
            })
            # также можно записать cookie 'last_enrolled' = slug
            response.set_cookie('last_enrolled', course_slug, max_age=30*24*60*60)
            return response
    # если не POST или форма не валидна — редирект на главную
    return redirect('courses:index')

# страница настроек
def settings_view(request):
    theme = request.COOKIES.get('theme', 'light')
    lang = request.COOKIES.get('lang', 'en')
    last = request.COOKIES.get('last_visited')
    try:
        last_list = json.loads(last) if last else []
    except Exception:
        last_list = []
    context = {
        'theme': theme,
        'lang': lang,
        'last_visited': last_list,
    }
    return render(request, 'courses/settings.html', context)

# быстрая смена темы (GET)
def set_theme(request, theme):
    # theme ожидается 'light' или 'dark'
    next_url = request.GET.get('next', '/')
    response = HttpResponseRedirect(next_url)
    response.set_cookie('theme', theme, max_age=365*24*60*60)  # год
    return response

# быстрая смена языка (GET)
def set_language(request, lang):
    # lang ожидается 'en' или 'ru'
    next_url = request.GET.get('next', '/')
    response = HttpResponseRedirect(next_url)
    response.set_cookie('lang', lang, max_age=365*24*60*60)  # год
    return response
