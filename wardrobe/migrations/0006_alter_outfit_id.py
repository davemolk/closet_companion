# Generated by Django 3.2.3 on 2021-07-30 16:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('wardrobe', '0005_item_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outfit',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
