from django.db import models
from mongoengine import Document, StringField
# Create your models here.

class Usuario(Document):

    nome = StringField(required=True)
    sexo = StringField(required=True)
