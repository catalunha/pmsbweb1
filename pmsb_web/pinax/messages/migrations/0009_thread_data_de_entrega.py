# Generated by Django 2.0.4 on 2018-07-11 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinax_messages', '0008_auto_20180709_2358'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='data_de_entrega',
            field=models.DateField(blank=True, null=True),
        ),
    ]
