# Generated by Django 4.1.8 on 2023-04-19 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='handle',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
