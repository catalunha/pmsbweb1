import os
import uuid

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from django.conf import settings
from django.core.management.base import BaseCommand
from questionarios.models import Questionario, Grupo, Pergunta, PossivelEscolha

cred = credentials.Certificate(os.path.join(settings.BASE_DIR, 'pmsb-22-to-firebase-adminsdk-nwnn3-b1cf350e9f.json'))
firebase_admin.initialize_app(cred)
db = firestore.client()
questionarioColl = db.collection('Questionario')
perguntaColl = db.collection('Pergunta')

def eixo(eixo):
  if (eixo=='res'):
    return {
      "id":"residuosolido",
      "nome":"Resíduo Sólido"
    }
  if (eixo=='aba'):
    return {
      "id":"abastecimentodeagua",
      "nome":"Abastecimento de água"
    }
  if (eixo=='dre'):
    return {
      "id":"drenagemurbana",
      "nome":"Drenagem Urbana"
    }
  if (eixo=='esg'):
    return {
      "id":"esgotamentosanitario",
      "nome":"Esgotamento Sanitário"
    }


def questionario_to_dict(questionario: Questionario, ordem:int):
    return {
        #"pk": '{}'.format(str(questionario.pk)),
        "nome": questionario.nome,
        "eixo":eixo('res'),
        "ultimaOrdem": ordem
    }
def pergunta_to_dict(pergunta: Pergunta, ordem: int, questionario: Questionario):
    return {
        #"pk": '{}'.format(str(pergunta.pk)),
        "eixo":eixo('res'),
        "titulo": pergunta.variavel,
        "textoMarkdown": pergunta.texto,
        "ordem": ordem,
        "questionario":{"id":'{}'.format(str(questionario.pk)),"nome":questionario.nome},
        "referencia": '{}'.format(str(uuid.uuid4())),
        "escolhas": {},
    }
def escolha_to_dict(texto: String, ordem: int):
    return {
        "key": True,
        "marcada": False,
        "texto":texto,
        "ordem":ordem,
    }
class Command(BaseCommand):
  help = "Migra app questionarios para firestore"

  def handle(self, *args, **options):
    tipoID=['','texto','arquivo','imagem','coordenada','numero',]
    tipoNome=['','Texto','Arquivo','Imagem','Coordenada','Número',]

    #residuo
    grupoID=Grupo.objects.get(pk="18bfa3aa-8fac-4025-a1e1-2dfef26c5c8d")
    #Esgotamento Sanitário
    #grupoID=Grupo.objects.get(pk="7e0b5b9d-a9bf-49b7-b946-9ea8b2cfd243")
    #Drenagem Urbana
    #grupoID=Grupo.objects.get(pk="b954d9c0-6edf-4b0a-8d24-e24019742bfa")
    #Abastecimento de Água
    #grupoID=Grupo.objects.get(pk="fe7445da-8d54-454b-a45b-d2cd5d6ba89f")
    
    
    for questionario in Questionario.objects.filter(grupo=grupoID):
      print("=====================================")
      print(questionario.nome)

      ordemPerg=0
      mapPerg={}
      for pergunta in questionario.perguntas:
        print("--------------------------------------")
        print("Tipo: {}".format(pergunta.tipo))
        print("Ordem: {}".format(ordemPerg))
        print("Titulo: {}".format(pergunta.variavel))
        mapPerg=pergunta_to_dict(pergunta,ordemPerg,questionario)
        pergunta_tipo = pergunta.cast()
        ordemPerg = ordemPerg + 1
        if pergunta.tipo==0 :
          ordemEsc=0
          print("Multipla: {}".format(pergunta_tipo.multipla))
          if pergunta_tipo.multipla :
            mapPerg["tipo"]={"id":"escolhamultipla","nome":"Escolha Múltipla"}
          else:
            mapPerg["tipo"]={"id":"escolhaunica","nome":"Escolha Única"}
          for escolha in pergunta_tipo.possiveis_escolhas.all():
            print("Escolha: {}".format(escolha.texto))
            mapPerg["escolhas"][str(escolha.pk)]=escolha_to_dict(escolha.texto,ordemEsc)
            ordemEsc = ordemEsc + 1
          mapPerg["ultimaOrdemEscolha"]: ordemEsc
        else:
          mapPerg["tipo"]={"id":tipoID[pergunta.tipo],"nome":tipoNome[pergunta.tipo]}
        print(mapPerg)    
        perguntaDoc = perguntaColl.document(str(pergunta.pk))
        perguntaDoc.set(mapPerg)
      mapQuest={}
      mapQuest=questionario_to_dict(questionario,ordemPerg)
      print(mapQuest)    
      questionarioDoc = questionarioColl.document(str(questionario.pk))
      questionarioDoc.set(mapQuest)


