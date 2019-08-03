import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


from django.conf import settings
from django.core.management.base import BaseCommand
from questionarios.models import Questionario, Grupo

cred = credentials.Certificate(os.path.join(settings.BASE_DIR, 'pmsb-22-to-firebase-adminsdk-nwnn3-b1cf350e9f.json'))
firebase_admin.initialize_app(cred)
db = firestore.client()
questionarioColl = db.collection('zpc-questionario')



def questionario_to_dict(questionario: Questionario):
    return {
        "pk": questionario.pk,
        "nome": questionario.nome,
        "eixo":{"id":"residuosolido","nome":"ressol"},
        "ultimaOrdem":0
    }

class Command(BaseCommand):
    help = "Migra app questionarios para firestore"

    def handle(self, *args, **options):

        questionarioDoc = questionarioColl.document()

        grupoID=Grupo.objects.get(pk="18bfa3aa-8fac-4025-a1e1-2dfef26c5c8d")
        for questionario in Questionario.objects.filter(grupo=grupoID):
            print(questionario_to_dict(questionario))
            questionarioDoc.set(questionario_to_dict(questionario))


