# Generated by Django 4.2.5 on 2024-04-04 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0043_rename_favoutire_ins_favourite_items_favourite_ins'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='average_rating',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='total_review',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
