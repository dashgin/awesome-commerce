from django.urls import path, include

from .views import LoginView, LogoutView, RegisterView, AccountDetailView, ProfileEditView, AddressEditView

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('detail/', AccountDetailView.as_view(), name="account-detail"),
    path('profile/edit/', ProfileEditView.as_view(), name="profile-edit"),
    path('address/<int:pk>/edit/', AddressEditView.as_view(), name="address-edit"),
]
