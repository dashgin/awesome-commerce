from collections.abc import Sequence
from typing import Any
from django.shortcuts import render
from django.views.generic import DetailView, ListView


from .models import Product


from urllib import request
from django.db.models import Q

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

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            query_name = Q(name__icontains=query)
            query_brand = Q(brand__icontains=query)
            query_sku = Q(sku__icontains=query) 
            query_description = Q(description__icontains=query) 
            query_color = Q(color__icontains=query) 
            query_size = Q(size__icontains=query)

            queryset = queryset.filter(
                query_name | query_brand | query_sku | query_description | query_color | query_size
            ).distinct()

        return queryset

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