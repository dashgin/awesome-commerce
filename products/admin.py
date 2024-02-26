from django.contrib import admin

from .models import Product, ProductViews, Category

admin.site.register(ProductViews)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'slug', 'view_count']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
