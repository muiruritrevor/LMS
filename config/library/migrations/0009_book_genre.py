# Generated by Django 5.1 on 2024-10-05 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_transaction_penalty_amount_transaction_penalty_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
