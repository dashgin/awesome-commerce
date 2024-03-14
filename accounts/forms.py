from typing import Any
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Profile, Address

User = get_user_model()


class RegisterForm(forms.Form):
    name = forms.CharField(label=_("Name"))
    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"), widget=forms.PasswordInput
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
    name = forms.CharField(label=_("Name"), required=False)

    class Meta:
        model = Profile
        fields = ["name", "birth_date", "phone", "profile_photo"]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }

    def save(self, commit=True):
        print(f"ProfileForm.save: {self.cleaned_data}")
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
