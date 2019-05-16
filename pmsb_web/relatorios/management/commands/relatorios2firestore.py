import os

import firebase_admin
from django.conf import settings
from django.core.management.base import BaseCommand
from firebase_admin import credentials
from firebase_admin import firestore
from relatorios.models import Relatorio, Bloco

cred = credentials.Certificate(os.path.join(settings.BASE_DIR, 'pmsb-22-to-0f2b559223f6.json'))
firebase_admin.initialize_app(cred)

db = firestore.client()

relatorios_ref = db.collection('relatorios')


def relatorio_to_dict(relatorio: Relatorio):
    return {
        "usuario": str(relatorio.usuario.pk),
        "titulo": relatorio.titulo,
        "descricao": relatorio.descricao,
        "criado_em": relatorio.criado_em,
        "editado_em": relatorio.editado_em,
        "fake_deletado": relatorio.fake_deletado,
        "fake_deletado_em": relatorio.fake_deletado_em,
    }


def bloco_to_dict(bloco: Bloco):
    return {
        "usuario": str(bloco.usuario.pk),
        "titulo": bloco.titulo,
        "descricao": bloco.descricao,
        "texto": bloco.texto,
        "ordem": bloco.ordem,
        "nivel": bloco.nivel,

        "criado_em": bloco.criado_em,
        "editado_em": bloco.editado_em,
        "fake_deletado": bloco.fake_deletado,
        "fake_deletado_em": bloco.fake_deletado_em,
    }


def add_bloco(parent_ref, bloco):
    bloco_ref = parent_ref.collection('blocos').document(str(bloco.pk))
    bloco_ref.set(bloco_to_dict(bloco))

    for bloco_filho in bloco.subblocos.all():
        add_bloco(bloco_ref, bloco_filho)


class Command(BaseCommand):
    help = "Migra app relatorios para firestore"

    def handle(self, *args, **options):
        """
        relatorios_docs = relatorios_ref.get()
        for doc in relatorios_docs:
            doc.reference.collection('testcoll').document("test").set({
                'number':1,
            })
            print(doc.to_dict())
        """
        for relatorio in Relatorio.objects.all():
            print(str(relatorio.pk))
            relatorio_ref = relatorios_ref.document(str(relatorio.pk))
            relatorio_ref.set(relatorio_to_dict(relatorio))
            for bloco in relatorio.blocos.filter(nivel_superior=None):
                add_bloco(relatorio_ref, bloco)
