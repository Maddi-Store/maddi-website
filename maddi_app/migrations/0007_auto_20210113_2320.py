# Generated by Django 3.1.4 on 2021-01-13 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maddi_app', '0006_shipping_receiver_city_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='date_paid',
            field=models.DateTimeField(null=True),
        ),
    ]
