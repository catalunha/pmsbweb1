# Generated by Django 2.0.4 on 2018-07-05 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='possivelescolha',
            name='pergunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='possiveis_escolhas', to='questionarios.PerguntaEscolha'),
        ),
    ]