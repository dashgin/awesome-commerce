from .services import CartService


def cart_items_count(request):
    cart_service = CartService(request)
    print("cart_items_count", cart_service.count())
    return {
        "cart_items_count": cart_service.count(),
    }