from django.contrib import admin
from django.urls import include, path

from django.conf.urls.static import static
from django.conf import settings
from pages.urls import urlpatterns as pages_urls


urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path("admin/", admin.site.urls),
    path("contact/", include("contact.urls"), name="contact"),
    path("accounts/", include("accounts.urls"), name="accounts"),
    path("products/", include("products.urls"), name="products"),
    path("cart/", include("cart.urls"), name="cart"),
]

urlpatterns += pages_urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.http import HttpResponse


def my_404_view(request, exception):
    return HttpResponse("404 Not Found, Tapilmadi :(")


handler404 = "config.urls.my_404_view"
