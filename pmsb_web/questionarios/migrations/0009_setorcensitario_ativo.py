# Generated by Django 2.1 on 2019-04-06 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionarios', '0008_auto_20181105_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='setorcensitario',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
    ]
