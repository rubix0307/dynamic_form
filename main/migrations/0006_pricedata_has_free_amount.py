# Generated by Django 5.0.6 on 2024-06-27 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_placetype_pricedata_place_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricedata',
            name='has_free_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]