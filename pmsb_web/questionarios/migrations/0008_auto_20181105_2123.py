# Generated by Django 2.0.4 on 2018-11-06 00:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('questionarios', '0007_auto_20180914_2044'),
    ]

    operations = [
        migrations.CreateModel(
            name='EscolhaRequisito',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fake_deletado', models.BooleanField(default=False)),
                ('fake_deletado_em', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PerguntaRequisito',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fake_deletado', models.BooleanField(default=False)),
                ('fake_deletado_em', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SetorCensitario',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fake_deletado', models.BooleanField(default=False)),
                ('fake_deletado_em', models.DateTimeField(blank=True, null=True)),
                ('nome', models.CharField(max_length=255, unique=True)),
                ('setor_superior', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subsetores', to='questionarios.SetorCensitario')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='questionario',
            name='perguntas',
        ),
        migrations.AddField(
            model_name='arquivoresposta',
            name='fake_deletado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='arquivoresposta',
            name='fake_deletado_em',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='coordenadaresposta',
            name='fake_deletado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='coordenadaresposta',
            name='fake_deletado_em',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='imagemresposta',
            name='fake_deletado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='imagemresposta',
            name='fake_deletado_em',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='localizacao',
            name='fake_deletado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='localizacao',
            name='fake_deletado_em',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='numeroresposta',
            name='fake_deletado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='numeroresposta',
            name='fake_deletado_em',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pergunta',
            name='fake_deletado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pergunta',
            name='fake_deletado_em',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='perguntadoquestionario',
            name='fake_deletado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='perguntadoquestionario',
            name='fake_deletado_em',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='possivelescolha',
            name='fake_deletado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='possivelescolha',
            name='fake_deletado_em',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='possivelescolharesposta',
            name='fake_deletado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='possivelescolharesposta',
            name='fake_deletado_em',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='questionario',
            name='fake_deletado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='questionario',
            name='fake_deletado_em',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respostapergunta',
            name='fake_deletado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='respostapergunta',
            name='fake_deletado_em',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respostaquestionario',
            name='fake_deletado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='respostaquestionario',
            name='fake_deletado_em',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='textoresposta',
            name='fake_deletado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='textoresposta',
            name='fake_deletado_em',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='unidademedida',
            name='fake_deletado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='unidademedida',
            name='fake_deletado_em',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='perguntarequisito',
            name='pergunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionarios.Pergunta'),
        ),
        migrations.AddField(
            model_name='perguntarequisito',
            name='pergunta_requisito',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionarios.PerguntaDoQuestionario'),
        ),
        migrations.AddField(
            model_name='escolharequisito',
            name='escolha_requisito',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionarios.PossivelEscolha'),
        ),
        migrations.AddField(
            model_name='escolharequisito',
            name='pergunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionarios.Pergunta'),
        ),
        migrations.AddField(
            model_name='escolharequisito',
            name='questionario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionarios.Questionario'),
        ),
        migrations.AddField(
            model_name='respostaquestionario',
            name='setor_censitario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='respostas', to='questionarios.SetorCensitario'),
        ),
        migrations.AlterUniqueTogether(
            name='perguntarequisito',
            unique_together={('pergunta', 'pergunta_requisito')},
        ),
        migrations.AlterUniqueTogether(
            name='escolharequisito',
            unique_together={('pergunta', 'questionario', 'escolha_requisito')},
        ),
    ]
