# Generated by Django 3.1.4 on 2021-01-13 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maddi_app', '0005_auto_20210113_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipping',
            name='receiver_city_name',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
