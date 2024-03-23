from typing import Any
from django.views.generic import TemplateView
from products.models import Category


class IndexView(TemplateView):
    template_name = "index.html"


class AboutView(TemplateView):
    template_name = "pages/about.html"
