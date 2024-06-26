# Generated by Django 4.2.5 on 2024-03-27 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0038_product_sizes_product_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product_sizes',
            name='product_variant',
        ),
        migrations.AlterField(
            model_name='product_sizes',
            name='product_price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product_sizes',
            name='product_size',
            field=models.CharField(choices=[('sm', 'Extra Small'), ('s', 'Small'), ('m', 'Medium'), ('l', 'Large'), ('xl', 'Extra Large'), ('xxl', 'Double Extra Large')], default=None, max_length=4),
        ),
    ]
