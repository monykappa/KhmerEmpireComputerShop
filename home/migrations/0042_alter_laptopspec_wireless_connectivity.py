# Generated by Django 4.2.6 on 2023-11-15 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_alter_laptopspec_port'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laptopspec',
            name='wireless_connectivity',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
