from django.core.management import BaseCommand

from customers.models import Customer


class Command(BaseCommand):
    help = 'Generate fake data for customers and products'

    def handle(self, *args, **kwargs):
        Customer.generate_fake_customers(20)
        self.stdout.write(self.style.SUCCESS('Successfully generated fake data.'))