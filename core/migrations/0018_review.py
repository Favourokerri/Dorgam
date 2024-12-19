# Generated by Django 5.1.4 on 2024-12-16 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_socialmedia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
