from .models import CartItem
from products.models import Product
from abc import ABC, abstractmethod


class AbstractCartService(ABC):

    @abstractmethod
    def add(self, product, quantity):
        raise NotImplementedError

    @abstractmethod
    def remove(self, product_id):
        raise NotImplementedError

    @abstractmethod
    def __len__(self):
        raise NotImplementedError

    @abstractmethod
    def get_total(self):
        raise NotImplementedError

    @abstractmethod
    def clear(self):
        raise NotImplementedError

    def is_empty(self):
        return len(self.cart_items) == 0

    def count(self):
        return len(self.cart_items)

class SessionCartService(AbstractCartService):
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

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __len__(self):
        """
        cart = SessionCartService(request)
        len(cart) ==>> 3
        """
        return sum(item["quantity"] for item in self.cart_items)

    def get_total(self):
        return sum(item["total_price"] for item in self.cart_items)

    def clear(self):
        del self.session["cart"]
        self.save()

    @property
    def cart_items(self):
        """
        {
            "1": {"quantity": 1},
            "2": {"quantity": 2},
        }==>>
        ==>>{
            "1": {"quantity": 1, "product": Product(id=1, name="Product 1", price=100), "total_price": 100},
            "2": {"quantity": 2, "product": Product(id=2, name="Product 2", price=200), "total_price": 400},
        }
        """
        cart_items_list = []
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]["product"] = product
            self.cart[str(product.id)]["total_price"] = (
                product.price * self.cart[str(product.id)]["quantity"]
            )
            cart_items_list.append(self.cart[str(product.id)])

        return cart_items_list


class DatabaseCartService(AbstractCartService):
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

    def remove(self, product_id):
        CartItem.objects.filter(
            user=self.user,
            product_id=product_id,
        ).delete()

    def __len__(self):
        return sum(item.quantity for item in self.cart_items)

    def get_total(self):
        return sum(item.total_price for item in self.cart_items)

    def clear(self):
        CartItem.objects.filter(user=self.user).delete()


class CartService:
    def __new__(cls, request):
        if request.user.is_authenticated:
            return DatabaseCartService(request)
        return SessionCartService(request)
