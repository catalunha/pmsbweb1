# Generated by Django 2.1 on 2019-05-13 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appblock',
            name='app_name',
            field=models.CharField(choices=[('django.contrib.admin', 'django.contrib.admin'), ('django.contrib.auth', 'django.contrib.auth'), ('django.contrib.contenttypes', 'django.contrib.contenttypes'), ('django.contrib.sessions', 'django.contrib.sessions'), ('django.contrib.messages', 'django.contrib.messages'), ('django.contrib.staticfiles', 'django.contrib.staticfiles'), ('rest_framework', 'rest_framework'), ('rest_framework.authtoken', 'rest_framework.authtoken'), ('corsheaders', 'corsheaders'), ('pinax.messages', 'pinax.messages'), ('widget_tweaks', 'widget_tweaks'), ('storages', 'storages'), ('rest_framework_swagger', 'rest_framework_swagger'), ('core', 'core'), ('conta', 'conta'), ('questionarios', 'questionarios'), ('relatorios', 'relatorios'), ('api', 'api')], max_length=255, unique=True),
        ),
    ]