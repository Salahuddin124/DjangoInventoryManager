# Generated by Django 5.0.4 on 2024-04-30 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_system', '0007_reservation_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
