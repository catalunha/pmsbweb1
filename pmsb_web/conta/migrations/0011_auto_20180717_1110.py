# Generated by Django 2.0.4 on 2018-07-17 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conta', '0010_auto_20180717_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='primeiro nome'),
        ),
    ]
