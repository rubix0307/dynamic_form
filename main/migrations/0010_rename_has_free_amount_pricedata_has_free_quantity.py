# Generated by Django 5.0.6 on 2024-06-28 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_rename_value_pricedata_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricedata',
            old_name='has_free_amount',
            new_name='has_free_quantity',
        ),
    ]