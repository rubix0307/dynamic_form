# Generated by Django 5.0.6 on 2024-06-27 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_pricedata_has_free_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricedata',
            old_name='description',
            new_name='name',
        ),
    ]
