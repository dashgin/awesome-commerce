import random
from django.core.management.base import BaseCommand, CommandError
from products.models import Product, ProductImage
import requests
import uuid
from django.core.files.base import ContentFile
from faker import Faker
from faker.providers import color, company
from django.utils.text import slugify
from django.core.files import File  # you need this somewhere

counter = 1

fake = Faker()

fake.add_provider(color)
fake.add_provider(company)


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("count", default=5, type=int)

    def handle(self, *args, **options):
        count = options["count"]
        self.generate_products(count)

        self.stdout.write(
            self.style.SUCCESS("Successfully populated products %s" % count)
        )

    def generate_product_images(self, product_id, count):
        """Generate product images 2 images for each product"""
        # example response: [{"id":"0","download_url":"https://picsum.photos/id/0/5000/3333"}]
        HEIGHT = 300
        WIDTH = 500
        global counter
        image_urls = [
            f"https://picsum.photos/{WIDTH}/{HEIGHT}.webp" for _ in range(count)
        ]

        for image_url in image_urls:
            url = f"{image_url}?random={counter}"
            counter += 1
            # download image
            response = requests.get(url)
            print(response, url)
            image = response.content
            file_name = uuid.uuid4().hex + ".webp"
            content_file = ContentFile(image)
            image_obj = ProductImage.objects.create(product_id=product_id)
            image_obj.image.save(file_name, content_file, save=True)

    def generate_products(self, count):
        products_to_bulk_create = []
        for _ in range(count):
            price = fake.random_int(100, 1000)
            discount_price = random.choice([None, fake.random_int(100, price)])
            name = fake.word()
            slug = slugify(name)
            product = Product(
                owner_id=1,
                name=name,
                slug=slug,
                brand=fake.company(),
                sku=uuid.uuid4().hex,
                price=price,
                quantity=fake.random_int(1, 100),
                color=fake.color_name(),
                size=fake.random_choices(
                    elements=("XS", "S", "M", "L", "XL"), length=1
                )[0],
                description=fake.text(),
                discount_price=discount_price,
            )
            products_to_bulk_create.append(product)
        Product.objects.bulk_create(products_to_bulk_create)
        for product in products_to_bulk_create:
            self.generate_product_images(product.id, 3)
