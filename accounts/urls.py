from django.urls import path

from django.contrib.auth import views as auth_views

from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    PasswordChangeView,
    AccountDetailView,
    ProfileEditView,
    AddressEditView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password/change/", PasswordChangeView.as_view(), name="password-change"),
    path("register/", RegisterView.as_view(), name="register"),
    path("detail/", AccountDetailView.as_view(), name="account-detail"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile-edit"),
    path("address/<int:pk>/edit/", AddressEditView.as_view(), name="address-edit"),
    path("password-reset/", auth_views.PasswordResetView.as_view(), name='password_reset'),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
