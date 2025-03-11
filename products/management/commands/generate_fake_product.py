from django.contrib.auth.models import User
from django.core.management import BaseCommand

from products.models import Product


class Command(BaseCommand):
    help = 'Generate fake data for customers and products'

    def handle(self, *args, **kwargs):
        owner = User.objects.all().first()
        Product.generate_fake_products(owner, 20)
        self.stdout.write(self.style.SUCCESS('Successfully generated fake data.'))