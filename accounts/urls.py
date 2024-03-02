from django.urls import path, include

from .views import LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    # path('register/', RegisterView.as_view(), name="ls"),
]
