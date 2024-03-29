# Generated by Django 2.1 on 2019-04-30 23:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('questionarios', '0012_auto_20190422_1302'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fake_deletado', models.BooleanField(default=False)),
                ('fake_deletado_em', models.DateTimeField(blank=True, null=True)),
                ('nome', models.CharField(max_length=255, unique=True)),
                ('descricao', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='questionario',
            name='grupo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='questionarios.Grupo'),
        ),
    ]
