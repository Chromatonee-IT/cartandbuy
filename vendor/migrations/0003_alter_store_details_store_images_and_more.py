# Generated by Django 4.2.5 on 2023-11-17 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_store_details_store_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store_details',
            name='store_images',
            field=models.ImageField(null=True, upload_to=None),
        ),
        migrations.AlterField(
            model_name='store_details',
            name='store_logo',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
    ]