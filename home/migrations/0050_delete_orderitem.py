# Generated by Django 4.2.6 on 2023-11-18 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0049_remove_order_ordered_products_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
