# Generated by Django 3.0.5 on 2021-07-11 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0009_remove_order_transaction_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='state',
        ),
    ]
