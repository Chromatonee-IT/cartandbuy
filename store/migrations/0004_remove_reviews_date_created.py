# Generated by Django 4.2.5 on 2023-11-25 02:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20231125_0253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviews',
            name='date_created',
        ),
    ]