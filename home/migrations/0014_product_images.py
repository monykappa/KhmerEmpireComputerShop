# Generated by Django 4.2.6 on 2023-10-27 10:54

from django.db import migrations, models
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_productspec_cpu_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.FileField(blank=True, upload_to=home.models.product_directory_path, validators=[home.models.validate_file_extension]),
        ),
    ]
