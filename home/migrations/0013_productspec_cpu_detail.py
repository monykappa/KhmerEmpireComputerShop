# Generated by Django 4.2.6 on 2023-10-27 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_rename_processor_productspec_cpu'),
    ]

    operations = [
        migrations.AddField(
            model_name='productspec',
            name='cpu_detail',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
