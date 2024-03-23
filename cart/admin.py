from django.contrib import admin

from .models import CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity", "total_price"]
    list_filter = ["product"]
    search_fields = ["product__name", "product__brand", "product__sku"]
    list_per_page = 10
