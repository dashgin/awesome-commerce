from django.contrib import admin

from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0


admin.site.register(ProductImage)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    prepopulated_fields = {
        "slug": (
            "brand",
            "name",
            "color",
            "size",
        )
    }
    list_display = [
        "name",
        "brand",
        "sku",
        "color",
        "size",
        "price",
        "discount_price",
        "category",
    ]
    search_fields = ["name", "brand", "sku", "description", "color", "size"]
    list_filter = ["category", "created_at"]
    list_editable = ["price", "discount_price"]
    list_per_page = 10
    date_hierarchy = "created_at"
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "owner",
                    "name",
                    "brand",
                    "sku",
                    "color",
                    "size",
                    "slug",
                    "category",
                    "description",
                    "quantity",
                    "price",
                    "discount_price",
                )
            },
        ),
        (
            "Date Information",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
    readonly_fields = ["created_at", "updated_at"]
