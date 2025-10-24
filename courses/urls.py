from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path('', views.index, name='index'),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('enroll/', views.enroll, name='enroll'),
    path('settings/', views.settings_view, name='settings'),
    path('set-theme/<str:theme>/', views.set_theme, name='set_theme'),  # быстрый переключатель темы
    path('set-language/<str:lang>/', views.set_language, name='set_language'),
]