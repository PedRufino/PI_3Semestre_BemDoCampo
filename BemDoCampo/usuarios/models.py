from django.utils import timezone
from datetime import timedelta
from django.db import models

DATE_NOW = timezone.now() - timedelta(hours=3)

class Usuarios(models.Model):
    user_id = models.IntegerField(unique=True, blank=False)
    nome = models.CharField(max_length=100, blank=False)
    sobrenome = models.CharField(max_length=100, blank=False)
    email = models.CharField(max_length=100, blank=False)
    documento = models.CharField(max_length=20, blank=False)
    contato = models.CharField(max_length=20, blank=False)
    data_nascimento = models.DateField(blank=False)
    cep = models.CharField(max_length=10, blank=False)
    endereco = models.CharField(max_length=100, blank=False)
    numero = models.IntegerField(blank=False)
    bairro = models.CharField(max_length=100, blank=False)
    cidade = models.CharField(max_length=100, blank=False)
    estado = models.CharField(max_length=2, blank=False)
    imagem_perfil = models.URLField(blank=True)
    data_cadastro = models.DateTimeField(default=DATE_NOW)

    class Meta:
        db_table = 'usuarios'
        managed = False

    def __str__(self):
        return self.nome