# Generated by Django 4.2.5 on 2024-02-25 16:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0008_remove_store_details_store_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='store_details',
            name='store_username',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
