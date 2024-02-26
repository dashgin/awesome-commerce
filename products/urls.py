from django.urls import path
from .views import (
    ProductListView,
    FeaturedProductListView,
    ProductCreateView,
    ProductDetailView,
    ProductDeleteView,
    # ProductUpdateView,
    CategoryListView,
    SearchProductListView,
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('featured/', FeaturedProductListView.as_view(), name='product-list-featured'),
    path('new/', ProductCreateView.as_view(), name='product-new'),
    path('<slug:slug>', ProductDetailView.as_view(), name="product-detail"),
    path('<slug:slug>/delete', ProductDeleteView.as_view(), name='product-delete'),
    # path('<slug:slug>/edit', ProductUpdateView.as_view(), name='product-update'),
    path('search/', SearchProductListView.as_view(), name="search"),
    path('category/<slug:slug>', CategoryListView.as_view(), name="products-by-category"),
]
