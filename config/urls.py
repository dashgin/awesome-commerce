from django.contrib import admin
from django.urls import include, path

from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.http import HttpResponse


def my_404_view(request, exception):
    return HttpResponse("404 Not Found, Tapilmadi :(")


handler404 = "config.urls.my_404_view"
