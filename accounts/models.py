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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    birth_date = models.DateField(_("Birth Date"), blank=True, null=True)
    phone = models.CharField(_("Phone"), blank=True, max_length=15)
    profile_photo = models.ImageField(_("Profile Photo"), upload_to="profile_photos", blank=True, null=True)
    
    def __str__(self):
        return self.user.name

    @property
    def get_profile_photo_url(self):
        if self.profile_photo and hasattr(self.profile_photo, "url"):
            return self.profile_photo.url
        return f"https://ui-avatars.com/api/?name={self.user.name}&size=300"
        return "/static/images/avatar.png"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    name = models.CharField(_("Name"), max_length=255)
    phone = models.CharField(_("Phone"), max_length=15)
    address = models.CharField(_("Address"), max_length=255)
    city = models.CharField(_("City"), max_length=255)
    country = models.CharField(_("Country"), max_length=255)
    zip_code = models.CharField(_("Zip Code"), max_length=255)

    def __str__(self):
        return self.address
