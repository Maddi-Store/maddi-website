# Generated by Django 3.1.4 on 2021-01-13 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maddi_app', '0003_auto_20210113_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipping',
            name='receiver_address',
            field=models.CharField(default=0, max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shipping',
            name='receiver_city',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shipping',
            name='receiver_postal_code',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
