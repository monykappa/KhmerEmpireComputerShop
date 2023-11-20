# Generated by Django 4.2.6 on 2023-11-19 11:26

from django.db import migrations, models
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0051_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand_category',
            name='logo',
            field=models.FileField(blank=True, null=True, upload_to=home.models.product_directory_path, validators=[home.models.validate_file_extension]),
        ),
    ]
