# Generated by Django 3.0.5 on 2021-07-10 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0002_profile_shippingaddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='alter_mobile_no',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mobile_no',
            field=models.CharField(max_length=10),
        ),
    ]
