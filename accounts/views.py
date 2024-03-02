from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView


class LoginView(DjangoLoginView):
    template_name = 'pages/login.html'
    next_page = reverse_lazy('index')


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('index')
    