from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, UpdateView
from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView,
)
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator

from .models import Address

from .forms import RegisterForm, ProfileForm, AddressForm


class LoginView(DjangoLoginView):
    template_name = "pages/login.html"
    next_page = reverse_lazy("index")
    redirect_authenticated_user = True


class LogoutView(LoginRequiredMixin, DjangoLogoutView):
    next_page = reverse_lazy("index")


class RegisterView(FormView):
    template_name = "pages/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    http_method_names = ["get", "post"]

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect("register")

    @method_decorator(sensitive_post_parameters(["password", "password2"]))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("index"))
        return super().dispatch(request, *args, **kwargs)


class AccountDetailView(LoginRequiredMixin, TemplateView):
    template_name = "pages/account.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = "pages/profile_edit.html"
    form_class = ProfileForm
    success_url = reverse_lazy("account-detail")
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context

    def get_object(self, queryset: QuerySet[Model] = None) -> Model:
        return self.request.user.profile

    def get_initial(self):
        initial = super().get_initial()
        initial["name"] = self.request.user.name
        return initial


class AddressEditView(LoginRequiredMixin, FormView):
    template_name = "pages/address_edit.html"
    success_url = reverse_lazy("account-detail")

    def get_object(self):
        if not hasattr(self, "object"):
            self.object = get_object_or_404(Address, pk=self.kwargs["pk"])
        return self.object

    def get_form(self):
        instance = self.get_object()
        form = AddressForm(data=self.request.POST or None, instance=instance)
        return form

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["address"] = self.get_object()
        return context
    
