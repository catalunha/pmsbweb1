# Generated by Django 2.0.4 on 2018-06-15 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionarios', '0002_auto_20180615_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerguntaArquivo',
            fields=[
                ('pergunta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='questionarios.Pergunta')),
            ],
            options={
                'abstract': False,
            },
            bases=('questionarios.pergunta',),
        ),
        migrations.CreateModel(
            name='PerguntaCoordenada',
            fields=[
                ('pergunta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='questionarios.Pergunta')),
            ],
            options={
                'abstract': False,
            },
            bases=('questionarios.pergunta',),
        ),
        migrations.CreateModel(
            name='PerguntaImagem',
            fields=[
                ('pergunta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='questionarios.Pergunta')),
            ],
            options={
                'abstract': False,
            },
            bases=('questionarios.pergunta',),
        ),
        migrations.CreateModel(
            name='PerguntaMultiplaEscolha',
            fields=[
                ('pergunta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='questionarios.Pergunta')),
            ],
            options={
                'abstract': False,
            },
            bases=('questionarios.pergunta',),
        ),
        migrations.CreateModel(
            name='PerguntaTexto',
            fields=[
                ('pergunta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='questionarios.Pergunta')),
            ],
            options={
                'abstract': False,
            },
            bases=('questionarios.pergunta',),
        ),
        migrations.CreateModel(
            name='PerguntaUnicaEscolha',
            fields=[
                ('pergunta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='questionarios.Pergunta')),
            ],
            options={
                'abstract': False,
            },
            bases=('questionarios.pergunta',),
        ),
        migrations.AlterField(
            model_name='pergunta',
            name='tipo',
            field=models.PositiveSmallIntegerField(editable=False),
        ),
    ]
