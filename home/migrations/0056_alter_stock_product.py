# Generated by Django 4.2.6 on 2023-11-23 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0055_alter_cartitem_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.product'),
        ),
    ]
