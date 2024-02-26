from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView


class LoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
    