# Generated by Django 4.2.6 on 2023-11-15 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_product_yt_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='yt_url',
        ),
        migrations.AddField(
            model_name='product',
            name='warranty',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
