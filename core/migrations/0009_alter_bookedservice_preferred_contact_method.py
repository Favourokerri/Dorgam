# Generated by Django 5.1.3 on 2024-12-05 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_bookedservice_preferred_contact_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookedservice',
            name='preferred_contact_method',
            field=models.CharField(choices=[('phone call', 'Phone call'), ('email', 'Email'), ('WhatsApp', 'WhatsApp')], default='email', max_length=10),
        ),
    ]
