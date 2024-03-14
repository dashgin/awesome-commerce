from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import decorators
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .admin_forms import UserAdminChangeForm, UserAdminCreationForm
from .models import Address, Profile

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "name", "is_superuser"]
    search_fields = ["name"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone", "birth_date"]
    search_fields = ["user__name"]
    ordering = ["id"] 


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["user", "address", "city", "country", "zip_code"]
    search_fields = ["user__name"]
    ordering = ["id"]
    list_filter = ["country"]