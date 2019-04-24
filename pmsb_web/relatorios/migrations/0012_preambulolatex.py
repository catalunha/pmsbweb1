# Generated by Django 2.1 on 2019-04-24 03:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('relatorios', '0011_auto_20190409_1910'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreambuloLatex',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fake_deletado', models.BooleanField(default=False)),
                ('fake_deletado_em', models.DateTimeField(blank=True, null=True)),
                ('titulo', models.CharField(max_length=255)),
                ('conteudo', models.TextField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]