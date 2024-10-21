from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from django.db import models
import os

DATE_NOW = timezone.now() - timedelta(hours=3)

class Produtos(models.Model):
    TIPOS_PRODUTOS = [
        ('fruta', 'Fruta'),
        ('verdura', 'Verdura'),
        ('grão', 'Grão'),
        ('laticinio', 'Laticínio'),
        ('carne', 'Carne'),
        ('peixe', 'Peixe'),
        ('cereal', 'Cereal'),
        ('temperos', 'Temperos'),
        ('oleo', 'Óleo'),
        ('bebida', 'Bebida'),
        ('doces', 'Doces'),
    ]
    
    TIPOS_UNIDADES = [
        ('kg', 'Quilograma (kg)'),
        ('g', 'Grama (g)'),
        ('l', 'Litro (l)'),
        ('ml', 'Mililitro (ml)'),
        ('un', 'Unidade (un)'),
        ('cx', 'Caixa (cx)'),
        ('pc', 'Pacote (pc)'),
    ]
    
    produto_id = models.CharField(max_length=255, blank=False)
    nome = models.CharField(max_length=100, blank=False)
    tipo_produto = models.CharField(max_length=100, choices=TIPOS_PRODUTOS, blank=False)
    quantidade = models.IntegerField(blank=False)
    tipo_unidade = models.CharField(max_length=5, choices=TIPOS_UNIDADES, blank=False)
    descricao = models.TextField(blank=False)
    produtor_id = models.IntegerField(blank=False)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    imagem_capa = models.FileField(blank=True)
    data_cadastro = models.DateTimeField(default=DATE_NOW)

    class Meta:
        db_table = 'produtos'
        managed = False

    def __str__(self):
        return self.nome
