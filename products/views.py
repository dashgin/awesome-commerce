from django.views.generic import DetailView


from .models import Product


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    slug_url_kwarg = "product_slug"
