# Generated by Django 3.2.3 on 2021-08-06 11:35

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('wardrobe', '0008_alter_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='images/itemdefault.jpg', force_format='JPEG', keep_meta=True, null=True, quality=75, size=[961, 1140], upload_to='images'),
        ),
    ]
