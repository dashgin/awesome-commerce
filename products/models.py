from django.db import models
from django.urls import reverse
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=50, null=True)
    slug = models.SlugField(max_length=50, unique=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

class Product(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, editable=False, max_length=110)
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True)
  
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    
    color = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @property
    def view_count(self):
        return ProductViews.objects.filter(product=self).count()


    def get_unique_slug(self):
        slug = slugify(self.name)
        # name = əşyalar
        # slug = esyalar
        # slug = esyalar-1
        # slug = esyalar-2

        unique_slug = slug
        counter = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{counter}'
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = _("products")
        verbose_name_plural = _("products")
        ordering = ['-created_at']


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images')

    def __str__(self):
        return self.product.title


class ProductViews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ip_address} in Post: {self.product.title}'


class UserProductWishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} in Wishlist: {self.product.title}'
