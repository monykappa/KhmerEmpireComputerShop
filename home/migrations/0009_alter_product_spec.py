# Generated by Django 4.2.6 on 2023-10-27 04:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_remove_productspec_product_product_spec'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='spec',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.productspec'),
        ),
    ]
