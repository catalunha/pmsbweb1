# Generated by Django 2.1 on 2019-04-09 22:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relatorios', '0010_auto_20190407_0051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='editor',
            name='bloco',
        ),
        migrations.RemoveField(
            model_name='editor',
            name='editor',
        ),
        migrations.RemoveField(
            model_name='editor',
            name='usuario',
        ),
        migrations.AlterField(
            model_name='bloco',
            name='editor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Editor',
        ),
    ]