from mongoengine import (
    EmbeddedDocumentField,
    EmbeddedDocument, 
    DateTimeField, 
    StringField, 
    FloatField,
    DateField, 
    DictField,
    ListField, 
    IntField, 
    Document, 
)

from django.utils import timezone
from datetime import timedelta

# Define o horário atual, se necessário
DATE_NOW = timezone.now() - timedelta(hours=3)

class FormaPagamento(EmbeddedDocument):
    id_cartao = StringField(max_length=36, required=True)
    nome_titular = StringField(max_length=100, required=True)
    numero_cartao = StringField(max_length=19, required=True)
    validade = StringField(max_length=5, required=True)
    documento = StringField(max_length=20, required=True)
    cvc = IntField(required=True)


TIPOS_USUARIOS = [
    ('consumidor', 'Consumidor'),
    ('agricultor', 'Agricultor'),
    ('pecuarista', 'Pecuarista'),
    ('cultivador', 'Cultivador'),
    ('comerciante', 'Comerciante'),
]

class MinhaTenda(EmbeddedDocument):
    id_tenda = StringField(required=True, max_length=255)
    nome_tenda = StringField(max_length=100, required=True)
    email = StringField(max_length=100, required=True)
    documento = StringField(max_length=20, required=True)
    contato = StringField(max_length=20, required=True)
    cep = StringField(max_length=10, required=True)
    endereco = StringField(max_length=100, required=True)
    numero = IntField(required=True)
    bairro = StringField(max_length=100, required=True)
    cidade = StringField(max_length=100, required=True)
    estado = StringField(max_length=2, required=True)
    imagem_tenda = StringField(required=False)
    tx_entrega = FloatField(default=0, required=False)
    tempo_entrega = DictField(required=False)
    data_cadastro = DateTimeField(default=DATE_NOW)
    avaliacoes_estrelas = DictField(field=IntField(), required=False)
    media_avaliacoes = FloatField(default=0, required=False)

    meta = {
        'collection': 'usuarios',
        'indexes': [
            {'fields': ['nome_tenda'], 'default_language': 'portuguese'}
        ]
    }

    def __str__(self):
        return f"{self.nome_tenda}"


class Usuarios(Document):
    user_id = IntField(unique=True, required=True)
    nome = StringField(max_length=100, required=True)
    sobrenome = StringField(max_length=100, required=True)
    email = StringField(max_length=100, required=True)
    documento = StringField(max_length=20, required=True)
    contato = StringField(max_length=20, required=True)
    data_nascimento = DateField(required=True)
    cep = StringField(max_length=10, required=True)
    endereco = StringField(max_length=100, required=True)
    numero = IntField(required=True)
    bairro = StringField(max_length=100, required=True)
    cidade = StringField(max_length=100, required=True)
    estado = StringField(max_length=2, required=True)
    imagem_perfil = StringField(required=False)
    tipo_usuario = StringField(choices=TIPOS_USUARIOS, default='consumidor', required=False)
    formas_pagamento = ListField(EmbeddedDocumentField(FormaPagamento), required=False)
    minha_tenda = EmbeddedDocumentField(MinhaTenda, required=False)
    data_cadastro = DateTimeField(default=DATE_NOW)

    meta = {
        'collection': 'usuarios',
    }

    def __str__(self):
        return f"{self.nome}"

