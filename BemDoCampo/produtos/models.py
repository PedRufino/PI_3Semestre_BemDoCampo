from mongoengine import (
    DateTimeField, 
    DecimalField, 
    StringField, 
    IntField, 
    Document, 
)

from datetime import (
    timedelta,
    datetime
)

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

class Produtos(Document):
    produto_id = StringField(required=True, max_length=255)
    nome = StringField(required=True, max_length=100)
    tipo_produto = StringField(choices=TIPOS_PRODUTOS, required=True)
    quantidade = IntField(required=True)
    tipo_unidade = StringField(choices=TIPOS_UNIDADES, required=True)
    descricao = StringField(required=True, max_length=500)
    produtor_id = IntField(required=True)
    valor = DecimalField(required=True, precision=2)
    imagem_capa = StringField(required=False)
    total_vendas = IntField(required=False)
    data_cadastro = DateTimeField(default=datetime.now() - timedelta(hours=3))
    
    meta = {
        'collection': 'produtos'
    }

    def __str__(self):
        return self.nome
