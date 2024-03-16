from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView

from ..models import Address

from ..forms import AddressForm

class AddressEditView(LoginRequiredMixin, FormView):
    template_name = "accounts/address_edit.html"
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
    
