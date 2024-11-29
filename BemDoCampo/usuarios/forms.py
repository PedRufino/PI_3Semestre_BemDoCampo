from allauth.account.forms import SignupForm
from django import forms


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label="Nome", required=True)
    last_name = forms.CharField(max_length=30, label="Sobrenome", required=True)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user


class ProfileForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())
    nome = forms.CharField(max_length=100, label="Nome", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'John',
        'id': 'name-input'
    }))
    sobrenome = forms.CharField(max_length=100, label="Sobrenome", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Snow',
        'id': 'lastname-input'
    }))
    email = forms.EmailField(max_length=100, label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': '@example.com',
        'id': 'email-input'
    }))
    documento = forms.CharField(max_length=20, label="Documento", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'maxlength': '14',
        'placeholder': 'CPF / CNPJ',
        'id': 'document-input'
    }))
    contato = forms.CharField(max_length=20, label="Contato", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'maxlength': '14',
        'placeholder': '(00) 00000-0000',
        'id': 'tel-input'
    }))
    data_nascimento = forms.DateField(label="Data de Nascimento", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'dd/mm/aaaa',
        'id': 'date-input'
    }))
    cep = forms.CharField(max_length=10, label="CEP", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'maxlength': '8',
        'placeholder': '00000-000',
        'id': 'cep-input'
    }))
    endereco = forms.CharField(max_length=100, label="Endereço", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Rua Jacinto Pinto',
        'id': 'logradouro-input'
    }))
    numero = forms.IntegerField(label="Número", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '69',
        'id': 'num-endereco-input'
    }))
    bairro = forms.CharField(max_length=100, label="Bairro", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'São João da Gala',
        'id': 'bairro-input'
    }))
    cidade = forms.CharField(max_length=100, label="Cidade", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Cubatão',
        'id': 'cidade-input'
    }))
    estado = forms.CharField(max_length=2, label="Estado", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'maxlength': '2',
        'placeholder': 'SP',
        'id': 'estado-input'
    }))
    imagem_perfil = forms.FileField(label="Imagem de Perfil", required=False, widget=forms.FileInput(attrs={
        'class': 'form-control',
        'id': 'inputGroupFile04',
        'aria-describedby': 'inputGroupFileAddon04',
        'aria-label': 'Upload'
    }))

    def __init__(self, *args, user_data=None, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(user_data, dict):
            for field in self.fields:
                if field in user_data:
                    self.fields[field].initial = user_data[field]


class PaymentsForm(forms.Form):
    cartao_id = forms.CharField(
        widget=forms.HiddenInput(attrs={
            'id': 'id_cartao',
            'name': 'id_cartao'
        }),
        required=False
    )
    nome_titular = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'stephan',
            'id': 'name-input'
        })
    )
    numero_cartao = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0000 0000 0000 0000',
            'id': 'number-input'
        })
    )
    validade = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '00/00',
            'id': 'validity-input'
        })
    )
    documento = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'maxlength': '14',
            'placeholder': 'CPF / CNPJ',
            'id': 'document-input'
        })
    )
    cvc = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'maxlength': '3',
            'placeholder': '000',
            'id': 'cvc-input'
        })
    )

    def __init__(self, *args, payment_data=None, **kwargs):
        super(PaymentsForm, self).__init__(*args, **kwargs)
        self.payment_data = payment_data

        if isinstance(self.payment_data, dict):
            for field in self.fields:
                if field in self.payment_data:
                    self.fields[field].initial = self.payment_data[field]


class MyTendaForm(forms.Form):
    nome_tenda = forms.CharField(max_length=100, label="Nome da Tenda", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Fazenda São Pedro ou Bia Hortifruti ',
        'id': 'tenda-input'
    }))
    tx_entrega = forms.DecimalField(
        label="Taxa de Entrega",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '4.99',
            'step':'0.01',
            'id': 'money-input'
        }),
        max_digits=10,
        decimal_places=2
    )
    email = forms.EmailField(max_length=100, label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': '@example.com',
        'id': 'email-input'
    }))
    documento = forms.CharField(max_length=20, label="Documento", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'maxlength': '14',
        'placeholder': 'CPF / CNPJ',
        'id': 'document-input'
    }))
    contato = forms.CharField(max_length=20, label="Contato", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'maxlength': '14',
        'placeholder': '(00) 00000-0000',
        'id': 'tel-input'
    }))
    cep = forms.CharField(max_length=10, label="CEP", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'maxlength': '8',
        'placeholder': '00000-000',
        'id': 'cep-input'
    }))
    endereco = forms.CharField(max_length=100, label="Endereço", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Rua Jacinto Pinto',
        'id': 'logradouro-input'
    }))
    numero = forms.IntegerField(label="Número", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '69',
        'id': 'num-endereco-input'
    }))
    bairro = forms.CharField(max_length=100, label="Bairro", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'São João da Gala',
        'id': 'bairro-input'
    }))
    cidade = forms.CharField(max_length=100, label="Cidade", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Cubatão',
        'id': 'cidade-input'
    }))
    estado = forms.CharField(max_length=2, label="Estado", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'maxlength': '2',
        'placeholder': 'SP',
        'id': 'estado-input'
    }))
    imagem_tenda = forms.FileField(label="Imagem Para Tenda:", required=False, widget=forms.FileInput(attrs={
        'class': 'form-control',
        'id': 'inputGroupFile04',
        'aria-describedby': 'inputGroupFileAddon04',
        'aria-label': 'Upload'
    }))
    
    def __init__(self, *args, user_data=None, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(user_data, dict):
            for field in self.fields:
                if field in user_data:
                    self.fields[field].initial = user_data[field]