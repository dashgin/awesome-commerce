from typing import Any
from django import forms
from django.utils.translation import gettext_lazy as _


class StyledWidgetMixin:
    extra_atrrs = {
        "class": "block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400"
    }

    def build_attrs(self, base_attrs, extra_attrs=None):
        return super().build_attrs(base_attrs, extra_attrs) | self.extra_atrrs


class StyledPasswordInput(StyledWidgetMixin, forms.PasswordInput):
    pass


class StyledTextInput(StyledWidgetMixin, forms.TextInput):
    pass


class StyledTextarea(StyledWidgetMixin, forms.Textarea):
    pass


class StyledEmailInput(StyledWidgetMixin, forms.EmailInput):
    pass


class StyledDateInput(StyledWidgetMixin, forms.DateInput):
    pass


class StyledClearableFileInput(StyledWidgetMixin, forms.ClearableFileInput):
    pass
