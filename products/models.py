from django.db import models
from django.contrib.auth.models import User
from faker import Faker

fake = Faker()


class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @staticmethod
    def generate_fake_products(owner, count=10):
        products = []
        for _ in range(count):
            products.append(Product(
                name=fake.word().capitalize(),
                owner=owner,
                sku=fake.unique.uuid4()[:8],
                price=round(fake.pydecimal(left_digits=4, right_digits=2, positive=True), 2),
                stock=fake.random_int(min=0, max=100)
            ))
        Product.objects.bulk_create(products)