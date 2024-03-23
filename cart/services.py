from .models import CartItem
from products.models import Product


class SessionCartService:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            self.session["cart"] = {}
            cart = self.session["cart"]

        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0}
        self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        {
            "1": {"quantity": 1},
            "2": {"quantity": 2},
        }==>>
        ==>>{
            "1": {"quantity": 1, "product": Product(id=1, name="Product 1", price=100)},
            "2": {"quantity": 2, "product": Product(id=2, name="Product 2", price=200)},
        }
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]["product"] = product
        for item in self.cart.values():
            item["total_price"] = item["product"].price * item["quantity"]
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total(self):
        return sum(item["total_price"] for item in self.cart.values())

    def clear(self):
        del self.session["cart"]
        self.save()

    def is_empty(self):
        return len(self.cart) == 0

    @property
    def cart_items(self):
        return list(self)


class DatabaseCartService:
    def __init__(self, request):
        self.user = request.user
        self.cart_items = CartItem.objects.filter(user=self.user)

    def add(self, product, quantity):
        cart_item = CartItem.objects.filter(user=self.user, product=product).first()
        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            CartItem.objects.create(
                user=self.user,
                product=product,
                quantity=quantity,
            )

    def remove(self, product):
        CartItem.objects.filter(
            user=self.user,
            product=product,
        ).delete()

    def __len__(self):
        return CartItem.objects.filter(user=self.user).count()

    def get_total(self):
        return sum(item.product.price * item.quantity for item in self.cart_items)

    def clear(self):
        CartItem.objects.filter(user=self.user).delete()

    def is_empty(self):
        return not CartItem.objects.filter(user=self.user).exists()


class CartService:
    def __new__(cls, request):
        if request.user.is_authenticated:
            return DatabaseCartService(request)
        return SessionCartService(request)
