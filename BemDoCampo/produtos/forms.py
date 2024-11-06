from django import forms
from . import models

class ProductForm(forms.Form):
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
    
    produtor_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    produto_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    nome = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Melancia',
            'id': 'name-input'
        }),
        max_length=100
    )
    tipo_produto = forms.ChoiceField(
        choices=TIPOS_PRODUTOS,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'produto-input'
        })
    )
    quantidade = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '5',
            'id': 'quantidade-input'
        })
    )
    tipo_unidade = forms.ChoiceField(
        choices=TIPOS_UNIDADES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'unidade-input'
        })
    )
    valor = forms.DecimalField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '24.99',
            'step':'0.01',
            'id': 'money-input'
        }),
        max_digits=10,
        decimal_places=2
    )
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Com sua polpa vermelha e suculenta, ela oferece um toque doce...',
            'rows': 1,
            'cols': 30,
            'id': 'descricao-input'
        })
    )
    imagem_capa = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'type': 'file',
            'id': 'inputGroupFile04',
            'aria-describedby': 'inputGroupFileAddon04',
            'aria-label': 'Upload'
        })
    )

    def __init__(self, *args, user_data=None, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(user_data, dict):
            for field in self.fields:
                if field in user_data:
                    self.fields[field].initial = user_data[field]
