# Generated by Django 4.2.6 on 2023-11-01 14:43

from django.db import migrations, models
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_delete_productrelatedimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_2',
            field=models.FileField(blank=True, upload_to=home.models.product_directory_path, validators=[home.models.validate_file_extension]),
        ),
        migrations.AddField(
            model_name='product',
            name='image_3',
            field=models.FileField(blank=True, upload_to=home.models.product_directory_path, validators=[home.models.validate_file_extension]),
        ),
        migrations.AddField(
            model_name='product',
            name='image_4',
            field=models.FileField(blank=True, upload_to=home.models.product_directory_path, validators=[home.models.validate_file_extension]),
        ),
        migrations.AddField(
            model_name='product',
            name='image_5',
            field=models.FileField(blank=True, upload_to=home.models.product_directory_path, validators=[home.models.validate_file_extension]),
        ),
        migrations.AddField(
            model_name='product',
            name='image_6',
            field=models.FileField(blank=True, upload_to=home.models.product_directory_path, validators=[home.models.validate_file_extension]),
        ),
    ]
