from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation

from .models import Profile, Address
from common import widgets

from common.widgets import StyledPasswordInput, StyledTextInput
from django.contrib.auth.forms import (
    AuthenticationForm as DjangoAuthenticationForm,
    PasswordChangeForm as DjangoPasswordChangeForm,
)

User = get_user_model()


class AuthenticationForm(DjangoAuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            StyledTextInput.extra_atrrs | {"placeholder": "John Doe"}
        )
        self.fields["password"].widget.attrs.update(
            StyledPasswordInput.extra_atrrs | {"placeholder": "********"}
        )


class PasswordChangeForm(DjangoPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs.update(
            StyledPasswordInput.extra_atrrs | {"placeholder": "********"}
        )
        self.fields["new_password1"].widget.attrs.update(
            StyledPasswordInput.extra_atrrs | {"placeholder": "********"}
        )
        self.fields["new_password2"].widget.attrs.update(
            StyledPasswordInput.extra_atrrs | {"placeholder": "********"}
        )


class RegisterForm(forms.Form):
    name = forms.CharField(
        label=_("Name"),
        widget=StyledTextInput(attrs={"placeholder": "John Doe"}),
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=StyledTextInput(attrs={"placeholder": "youremail@domain.com"}),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=StyledPasswordInput(attrs={"placeholder": "********"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=StyledPasswordInput(attrs={"placeholder": "********"}),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("Email already exists"))
        return email

    def clean_password2(self):
        password = self.cleaned_data["password"]
        password2 = self.cleaned_data["password2"]
        if password != password2:
            raise forms.ValidationError(_("Passwords do not match"))
        return password2

    def save(self):
        return User.objects.create_user(
            name=self.cleaned_data["name"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )


class ProfileForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Name"),
        required=False,
        widget=widgets.StyledTextInput(attrs={"placeholder": "John Doe"}),
    )

    class Meta:
        model = Profile
        fields = ["name", "birth_date", "phone", "profile_photo"]
        widgets = {
            "birth_date": widgets.StyledDateInput(attrs={"type": "date"}),
            "phone": widgets.StyledTextInput(attrs={"placeholder": "1234567890"}),
            "profile_photo": widgets.StyledClearableFileInput(
                attrs={"class": "hidden"}
            ),
        }

    def save(self, commit=True):
        user_name = self.cleaned_data.pop("name")
        profile = super().save(commit=False)
        user = self.instance.user
        user.name = user_name
        user.save()
        if commit:
            profile.save()
        return profile


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["address", "city", "country", "zip_code", "name", "phone"]

        widgets = {
            "address": widgets.StyledTextarea(attrs={"placeholder": "1234 Main St"}),
            "city": widgets.StyledTextInput(attrs={"placeholder": "City"}),
            "country": widgets.StyledTextInput(attrs={"placeholder": "Country"}),
            "zip_code": widgets.StyledTextInput(attrs={"placeholder": "12345"}),
            "name": widgets.StyledTextInput(attrs={"placeholder": "John Doe"}),
            "phone": widgets.StyledTextInput(attrs={"placeholder": "1234567890"}),
        }
