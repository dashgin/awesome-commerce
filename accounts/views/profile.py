from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView


from ..forms import ProfileForm


class AccountDetailView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/account.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = "accounts/profile_edit.html"
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

