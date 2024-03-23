from django.urls import path
from .views import  CartView, AddToCartView

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("add/", AddToCartView.as_view(), name="add_to_cart"),
]   