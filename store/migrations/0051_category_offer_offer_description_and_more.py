# Generated by Django 4.2.5 on 2024-05-02 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0050_midcategory_midcategory_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category_offer',
            name='offer_description',
            field=models.CharField(default='', max_length=80),
        ),
        migrations.AddField(
            model_name='category_offer',
            name='offer_heading',
            field=models.CharField(default='', max_length=40),
        ),
    ]