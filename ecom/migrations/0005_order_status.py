# Generated by Django 3.0.5 on 2021-07-10 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0004_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]