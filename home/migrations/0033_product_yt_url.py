# Generated by Django 4.2.6 on 2023-11-13 12:08

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0032_remove_product_yt_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='yt_url',
            field=embed_video.fields.EmbedVideoField(blank=True, null=True),
        ),
    ]
