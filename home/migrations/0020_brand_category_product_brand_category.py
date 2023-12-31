# Generated by Django 4.2.6 on 2023-10-30 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_alter_laptopspec_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='brand_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='brand_category',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brand_category', to='home.brand_category'),
        ),
    ]
