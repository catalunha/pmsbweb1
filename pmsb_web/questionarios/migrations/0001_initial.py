# Generated by Django 2.0.4 on 2018-06-12 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import questionarios.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArquivoResposta',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('arquivo', models.FileField(upload_to=questionarios.models.caminho_para_arquivos)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CoordenadaResposta',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImagemResposta',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('imagem', models.ImageField(upload_to=questionarios.models.caminho_para_imagens)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Localizacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('altitude', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='NumeroResposta',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('numero', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pergunta',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('variavel', models.CharField(max_length=255)),
                ('texto', models.TextField()),
                ('tipo', models.PositiveSmallIntegerField(choices=[(0, 'Unica Escolha'), (1, 'Multipla Escolha'), (2, 'Texto'), (3, 'Arquivo'), (4, 'Imagem'), (5, 'Coordenada'), (6, 'Numero')])),
            ],
            options={
                'verbose_name': 'Pergunta',
                'verbose_name_plural': 'Perguntas',
                'ordering': ('tipo',),
            },
        ),
        migrations.CreateModel(
            name='PerguntaDoQuestionario',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ordem', models.PositiveSmallIntegerField()),
                ('pergunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionarios.Pergunta')),
            ],
            options={
                'ordering': ('questionario', 'ordem', 'pergunta'),
            },
        ),
        migrations.CreateModel(
            name='PossivelEscolha',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('texto', models.TextField()),
                ('pergunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='possiveis_escolhas', to='questionarios.Pergunta')),
            ],
            options={
                'verbose_name': 'Possivel Escolha',
                'verbose_name_plural': 'Possiveis Escolhas',
            },
        ),
        migrations.CreateModel(
            name='PossivelEscolhaResposta',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('possivel_escolha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionarios.PossivelEscolha')),
            ],
        ),
        migrations.CreateModel(
            name='Questionario',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('publicado', models.BooleanField(default=False)),
                ('perguntas', models.ManyToManyField(related_name='questionarios', through='questionarios.PerguntaDoQuestionario', to='questionarios.Pergunta')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Questionario',
                'verbose_name_plural': 'Questionarios',
            },
        ),
        migrations.CreateModel(
            name='RespostaPergunta',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('localizacao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='questionarios.Localizacao')),
                ('pergunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionarios.Pergunta')),
            ],
            options={
                'verbose_name': 'Resposta Pergunta',
                'verbose_name_plural': 'Respostas Perguntas',
            },
        ),
        migrations.CreateModel(
            name='RespostaQuestionario',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('questionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respostas', to='questionarios.Questionario')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Resposta Questionario',
                'verbose_name_plural': 'Respostas Questionarios',
            },
        ),
        migrations.CreateModel(
            name='TextoResposta',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('texto', models.TextField()),
                ('resposta_pergunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='textos', to='questionarios.RespostaPergunta')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='respostapergunta',
            name='resposta_questionario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionarios.RespostaQuestionario'),
        ),
        migrations.AddField(
            model_name='possivelescolharesposta',
            name='resposta_pergunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='escolhas', to='questionarios.RespostaPergunta'),
        ),
        migrations.AddField(
            model_name='perguntadoquestionario',
            name='questionario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionarios.Questionario'),
        ),
        migrations.AddField(
            model_name='pergunta',
            name='possivel_escolha_requisito',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pre_requisito_de', to='questionarios.PossivelEscolha'),
        ),
        migrations.AddField(
            model_name='numeroresposta',
            name='resposta_pergunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='numeros', to='questionarios.RespostaPergunta'),
        ),
        migrations.AddField(
            model_name='imagemresposta',
            name='resposta_pergunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagens', to='questionarios.RespostaPergunta'),
        ),
        migrations.AddField(
            model_name='coordenadaresposta',
            name='coordenada',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='questionarios.Localizacao'),
        ),
        migrations.AddField(
            model_name='coordenadaresposta',
            name='resposta_pergunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coordenadas', to='questionarios.RespostaPergunta'),
        ),
        migrations.AddField(
            model_name='arquivoresposta',
            name='resposta_pergunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arquivos', to='questionarios.RespostaPergunta'),
        ),
        migrations.AlterUniqueTogether(
            name='respostapergunta',
            unique_together={('resposta_questionario', 'pergunta')},
        ),
        migrations.AlterUniqueTogether(
            name='possivelescolharesposta',
            unique_together={('resposta_pergunta', 'possivel_escolha')},
        ),
        migrations.AlterUniqueTogether(
            name='perguntadoquestionario',
            unique_together={('questionario', 'pergunta')},
        ),
    ]
