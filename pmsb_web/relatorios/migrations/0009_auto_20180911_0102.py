# Generated by Django 2.1 on 2018-09-11 04:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relatorios', '0008_auto_20180910_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloco',
            name='editor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
