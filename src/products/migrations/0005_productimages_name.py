# Generated by Django 4.1.8 on 2023-05-03 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_productimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimages',
            name='name',
            field=models.CharField(blank=True, max_length=125, null=True),
        ),
    ]