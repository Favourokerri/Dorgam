# Generated by Django 5.1.3 on 2024-12-05 10:48

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', django_ckeditor_5.fields.CKEditor5Field()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='enter service image', upload_to='')),
                ('name_of_service', models.CharField(max_length=200)),
                ('detail', django_ckeditor_5.fields.CKEditor5Field()),
            ],
        ),
    ]
