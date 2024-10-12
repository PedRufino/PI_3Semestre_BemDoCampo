import uuid
from django.db import models
from datetime import datetime

# class Localizacao(models.Model):
#     cidade = models.CharField(max_length=100, blank=False)
#     estado = models.CharField(max_length=100, blank=False)

    # def __str__(self):
    #     return f"{self.cidade}, {self.estado}"

class Produtos(models.Model):
    
    nome = models.CharField(max_length=100, blank=False)
    tipo = models.CharField(max_length=100, blank=False)
    quantidade = models.IntegerField(blank=False)
    unidade = models.CharField(max_length=50, blank=False)
    descricao = models.TextField(blank=True)
    produtor_id = models.CharField(max_length=100, blank=False)
    imagem_capa = models.URLField(blank=True)
    imagens = models.JSONField(blank=True, default=list)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'produtos'  # Nome da coleção no MongoDB
        managed = False  # Para não tentar gerenciar as migrações do Django

    def __str__(self):
        return self.nome