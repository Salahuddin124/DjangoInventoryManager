# Generated by Django 5.0.4 on 2024-04-30 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_system', '0006_reservation_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='image',
            field=models.ImageField(default=33, upload_to='reservation_images/'),
            preserve_default=False,
        ),
    ]
