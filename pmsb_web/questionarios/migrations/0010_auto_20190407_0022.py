# Generated by Django 2.1 on 2019-04-07 03:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionarios', '0009_setorcensitario_ativo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questionario',
            options={'ordering': ('nome',), 'verbose_name': 'Questionario', 'verbose_name_plural': 'Questionarios'},
        ),
    ]