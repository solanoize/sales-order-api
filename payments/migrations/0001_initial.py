# Generated by Django 5.1.7 on 2025-03-09 14:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('method', models.CharField(choices=[('cash', 'Cash'), ('credit_card', 'Credit Card'), ('debit_card', 'Debit Card'), ('bank_transfer', 'Bank Transfer'), ('digital_wallet', 'Digital Wallet')], max_length=20)),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('sales_order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='orders.salesorder')),
            ],
        ),
    ]
