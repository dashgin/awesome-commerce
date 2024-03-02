from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    # Remove fields that are not needed
    first_name = None
    last_name = None
    username = None

    email = models.EmailField(_("email Address"), unique=True)
    name = models.CharField(_("Name of User"), blank=True, null=True, max_length=255)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def get_absolute_url(self):
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(_("Birth Date"), blank=True, null=True)
    phone = models.CharField(_("Phone"), blank=True, max_length=15)
    profile_photo = models.ImageField(_("Profile Photo"), upload_to="profile_photos", blank=True, null=True)
    bio = models.TextField(_("Bio"), blank=True, null=True)
    
    def __str__(self):
        return self.name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(_("Address"), max_length=255)
    city = models.CharField(_("City"), max_length=255)
    country = models.CharField(_("Country"), max_length=255)
    zip_code = models.CharField(_("Zip Code"), max_length=255)

    def __str__(self):
        return self.address
