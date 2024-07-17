"""Модуль, с определением функций-обработчиков приложения pages."""


from django.shortcuts import render
from django.views.generic import TemplateView


class About(TemplateView):
    """Обрабатывает статичную страницу 'О проекте'."""

    template_name = 'pages/about.html'


class Rules(TemplateView):
    """Обрабатывает статичную страницу 'Правила'."""

    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    """Обрабатывает страницу с ошибкой '404 Not Found'."""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """Обрабатывает страницу с ошибкой '403 Forbidden'."""
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    """Обрабатывает страницу с ошибкой 'Internal Server Error'."""
    return render(request, 'pages/500.html', status=500)
