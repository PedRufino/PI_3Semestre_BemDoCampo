from allauth.account.forms import SignupForm
from django.forms import fields
from .models import Usuarios
from django import forms


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label="Nome")
    last_name = forms.CharField(max_length=30, label="Sobrenome")

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user


from django import forms
from .models import Usuarios

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = (
            "user_id",
            "nome",
            "sobrenome",
            "email",
            "documento",
            "contato",
            "data_nascimento",
            "cep",
            "endereco",
            "numero",
            "bairro",
            "cidade",
            "estado",
        )
        widgets = {
            'user_id': forms.HiddenInput({
                'value':'{{ user_id }}'
            }),
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'John',
                'id': 'name-input'
            }),
            'sobrenome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Snow',
                'id': 'lastname-input'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '@example.com',
                'id': 'email-input'
            }),
            'documento': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '14',
                'placeholder': 'CPF / CNPJ',
                'id': 'document-input'
            }),
            'contato': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '14',
                'placeholder': '(00) 00000-0000',
                'id': 'tel-input'
            }),
            'data_nascimento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'dd/mm/aaaa',
                'id': 'date-input'
            }),
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '8',
                'placeholder': '00000-000',
                'id': 'cep-input'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rua Jacinto Pinto',
                'id': 'logradouro-input'
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '69',
                'id': 'num-endereco-input'
            }),
            'bairro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'São João da Gala',
                'id': 'bairro-input'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cubatão',
                'id': 'cidade-input'
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '2',
                'placeholder': 'SP',
                'id': 'estado-input'
            }),
        }

    def __init__(self, *args, user_data=None, **kwargs):
        self.user_data = user_data
        super(ProfileForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            if isinstance(self.user_data, dict) and field in self.user_data:
                self.fields[field].initial = self.user_data[field]
