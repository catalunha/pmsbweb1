# Generated by Django 2.0.4 on 2018-07-14 22:12

from django.db import migrations, models
import pinax.messages.models


class Migration(migrations.Migration):

    dependencies = [
        ('pinax_messages', '0009_thread_data_de_entrega'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='file_upload',
            field=models.FileField(blank=True, null=True, upload_to=pinax.messages.models.documento_upload),
        ),
    ]
