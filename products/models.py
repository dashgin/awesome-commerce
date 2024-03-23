from django.db import models
from django.urls import reverse
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


"""
products_category
| CategoryID    | ParentID  | Name          | Slug          |
| 1             | NULL      | Electronics   | electronics   |
| 2             | 1(FK)     | Mobile Phones | mobile-phones |
| 3             | 1(FK)     | Laptops       | laptops       |
| 4             | NULL      | Vehicles      | vehicles      |
| 5             | 4(FK)     | Cars          | cars          |
| 6             | 4(FK)     | Motorcycles   | motorcycles   |
"""

class Category(models.Model):
    # parent = models.ForeignKey(
    #     "self",
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    #     related_name="children",
    # )
    name = models.CharField(max_length=50, null=True)
    slug = models.SlugField(max_length=50, unique=True, null=True)
    image = models.ImageField(upload_to="categories/images", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")


class Product(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=110)
    sku = models.CharField(max_length=50, null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True)

    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)

    color = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # @property
    # def view_count(self):
    #     return ProductViews.objects.filter(product=self).count()

    def get_unique_slug(self):
        slug_text = f"{self.name} {self.color}"
        slug = slugify(slug_text)
        unique_slug = slug
        counter = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.id})

    @property
    def variants(self):
        _variants = Product.objects.filter(sku=self.sku)
        variants = {
            "colors": {},
            "sizes": {},
        }
        for variant in _variants:
            if variant.color and variant.color not in variants["colors"]:
                variants["colors"][variant.color] = variant.get_absolute_url()
            if variant.color == self.color:
                if variant.size and variant.size not in variants["sizes"]:
                    is_available = variant.quantity > 0
                    variants["sizes"][variant.size] = (variant.id, is_available)
        return variants


    class Meta:
        verbose_name = _("products")
        verbose_name_plural = _("products")
        ordering = ["-created_at"]


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/images")

    def __str__(self):
        return self.product.name


# class ProductViews(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     ip_address = models.GenericIPAddressField(null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.ip_address} in Post: {self.product.name}"


# class UserProductWishlist(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} in Wishlist: {self.product.name}"


