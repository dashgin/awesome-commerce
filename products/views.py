from collections.abc import Sequence
from typing import Any
from django.views.generic import DetailView, ListView


from .models import Product


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    slug_url_kwarg = "product_slug"

class ProductListView(ListView):
    template_name = "products/product_list.html"
    model = Product
    context_object_name = "products"    
    paginate_by = 3
    max_paginate_by = 120
    ordering = "id"

    def get_paginate_by(self, queryset) -> Any:

        limit = self.request.GET.get("limit", self.paginate_by)
        try:
            limit = int(limit)
            if limit > self.max_paginate_by:
                limit = self.max_paginate_by
        except ValueError:
            limit = self.paginate_by
       
        return limit
    

    def get_ordering(self) -> str:
        ordering = self.request.GET.get("ordering", self.ordering)
        if ordering not in [ "-id", "id", "price", "-price"]:
            ordering = self.ordering
        return ordering