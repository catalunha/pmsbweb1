# Generated by Django 2.0.4 on 2018-07-30 00:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import pinax.messages.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sent_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.TextField()),
                ('file_upload', models.FileField(blank=True, null=True, upload_to=pinax.messages.models.documento_upload)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-sent_at',),
            },
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=150, verbose_name='Título da Tarefa')),
                ('data_de_entrega', models.DateField(blank=True, null=True, verbose_name='Prazo')),
                ('data_finalizada', models.DateField(blank=True, null=True, verbose_name='Finalizada em')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserThread',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('unread', models.BooleanField()),
                ('deleted', models.BooleanField()),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pinax_messages.Thread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='thread',
            name='users',
            field=models.ManyToManyField(through='pinax_messages.UserThread', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='pinax_messages.Thread'),
        ),
    ]
