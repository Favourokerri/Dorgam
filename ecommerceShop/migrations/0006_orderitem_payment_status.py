# Generated by Django 5.1.4 on 2024-12-15 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceShop', '0005_order_orderitem_order_order_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='payment_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('PAID', 'Paid'), ('FAILED', 'Failed')], default='PENDING', max_length=10),
        ),
    ]