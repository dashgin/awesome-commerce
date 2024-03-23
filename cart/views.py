from django.contrib import messages
from django.views.generic import ListView, FormView

from .forms import AddToCartForm
from .services import CartService


class AddToCartView(FormView):
    form_class = AddToCartForm

    def form_valid(self, form):
        cart_service = CartService(self.request)
        cart_service.add(
            product=form.cleaned_data["product"],
            quantity=form.cleaned_data["quantity"],
        )
        messages.success(self.request, "Product added to cart")
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return self.request.META.get("HTTP_REFERER", "/")


class CartView(ListView):
    template_name = "cart/cart.html"
    context_object_name = "cart"
    paginate_by = 10

    def get_queryset(self):
        cart_service = CartService(self.request)
        return cart_service.cart_items
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_total"] = CartService(self.request).get_total()
        return context
