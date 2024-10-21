from django import forms
from . import models


class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Produtos
        fields = (
            "produto_id",
            "nome",
            "tipo_produto",
            "quantidade",
            "tipo_unidade",
            "valor",
            "descricao",
            "produtor_id",
            "imagem_capa"
        )
        widgets = {
            'produtor_id': forms.HiddenInput(),
            'produto_id': forms.HiddenInput(),
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Melancia',
                'id': 'name-input'
            }),
            'tipo_produto': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Fruta',
                'id': 'produto-input'
            }),
            'tipo_unidade': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Quilograma (kg)',
                'id': 'unidade-input'
            }),
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '5',
                'id': 'quantidade-input'
            }),
            'valor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '24,99',
                'id': 'money-input'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Com sua polpa vermelha e suculenta, ela oferece um toque doce...',
                'rows': 1,
                'cols': 30,
                'id': 'descricao-input'
            }),
            'imagem_capa': forms.FileInput(attrs={
                'class': 'form-control',
                'type': 'file',
                'id': 'inputGroupFile04',
                'aria-describedby': 'inputGroupFileAddon04',
                'aria-label': 'Upload'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)