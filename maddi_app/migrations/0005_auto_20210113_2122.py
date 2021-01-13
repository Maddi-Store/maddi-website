# Generated by Django 3.1.4 on 2021-01-13 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maddi_app', '0004_auto_20210113_1720'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='destination_address',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='destination_city',
        ),
        migrations.AlterField(
            model_name='shipping',
            name='date_arrived',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='date_shipped',
            field=models.DateTimeField(null=True),
        ),
    ]
