# Generated by Django 4.2.5 on 2024-03-02 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0031_customer_email_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email_verification_code',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
