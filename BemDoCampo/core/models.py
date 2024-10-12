from django.db import models
from datetime import datetime
# Create your models here.

from mongoengine import Document, StringField, IntField, ListField, DictField, DateTimeField
import datetime

class Localizacao(Document):
    cidade = StringField(required=True)
    estado = StringField(required=True)

class Alimento(Document):
    alimento_id = StringField(required=True)
    nome = StringField(required=True)
    tipo = StringField(required=True)
    quantidade = IntField(required=True)
    unidade = StringField(required=True)
    descricao = StringField()
    produtor_id = StringField(required=True)
    localizacao = DictField()  # pode ser Localizacao() se preferir usar o modelo separado
    imagem_capa = StringField()
    imagens = ListField(StringField())
    data_cadastro = DateTimeField(default=datetime.datetime.utcnow)
