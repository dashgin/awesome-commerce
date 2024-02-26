from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView

from .models import Product, Category, ProductViews
from .forms import ProductCreateForm


class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    paginate_by = 36

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all().order_by('-created_at')
        context['categories_list'] = Category.objects.all()
        return context


class FeaturedProductListView(ListView):
    queryset = Product.objects.filter(featured=True).order_by('-created_at')
    template_name = "product/product_list.html"
    paginate_by = 24

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'

    def get_object(self, *args, **kwargs):
        obj = super().get_object()
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0] if x_forwarded_for else self.request.META.get('REMOTE_ADDR')
        ProductViews.objects.get_or_create(product=obj, ip_address=ip)
        return obj



class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'product/product_delete.html'
    slug_field = 'slug'
    success_message = 'Elan müvəffəqiyyətlə silindi'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ProductDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.id})

    def test_func(self):
        book = self.get_object()
        if self.request.user == book.owner:
            return True
        return False


class ProductCreateView(LoginRequiredMixin, CreateView):
    form_class = ProductCreateForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    template_name = 'product/product_add.html'
    success_url = '/'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['categories_list'] = Category.objects.all()
        return context


class CategoryListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'
    paginate_by = 24

    def get_queryset(self, *args, **kwargs):
        products = Product.objects.filter(category__slug=self.kwargs['slug'])
        return products


class SearchProductListView(ListView):
    template_name = "product/product_search.html"
    paginate_by = 36
    context_object_name = 'products'

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q', None)
        qs = Product.objects.all()
        if query:
            return qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(price__icontains=query) |
                Q(author__icontains=query)
            ).distinct()
        return qs.none()

