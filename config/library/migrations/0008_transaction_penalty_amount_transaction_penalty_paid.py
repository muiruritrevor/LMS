# Generated by Django 5.1 on 2024-10-05 10:53

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_alter_transaction_return_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='penalty_amount',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=5),
        ),
        migrations.AddField(
            model_name='transaction',
            name='penalty_paid',
            field=models.BooleanField(default=False),
        ),
    ]
