from django.db import models
from faker import Faker

fake = Faker()


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def generate_fake_customers(count=10):
        customers = []
        for _ in range(count):
            customers.append(Customer(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                phone=fake.phone_number()
            ))
        Customer.objects.bulk_create(customers)