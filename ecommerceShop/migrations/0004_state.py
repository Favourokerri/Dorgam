# Generated by Django 5.1.4 on 2024-12-14 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceShop', '0003_cart_cartitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('shipping_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('delivery_available', models.BooleanField(default=True)),
            ],
        ),
    ]
