# Generated by Django 3.1.4 on 2021-01-13 17:12

from django.db import migrations
import smartfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('maddi_app', '0007_auto_20210113_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='image',
            field=smartfields.fields.ImageField(null=True, upload_to='payment'),
        ),
    ]
