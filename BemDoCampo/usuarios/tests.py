from django.test import TestCase
from .forms import CustomSignupForm, ProfileForm, PaymentsForm

class CustomSignupFormTests(TestCase):
    def test_formulario_valido(self):
        form_data = {
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        form = CustomSignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_formulario_invalido_campos_ausentes(self):
        form_data = {
            'email': '',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': '',
            'last_name': ''
        }
        form = CustomSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)


class ProfileFormTests(TestCase):
    def test_formulario_de_perfil_valido(self):
        form_data = {
            'user_id': 1,
            'nome': 'John',
            'sobrenome': 'Doe',
            'email': 'john.doe@example.com',
            'documento': '12345678909',
            'contato': '(00) 00000-0000',
            'data_nascimento': '1990-01-01',
            'cep': '12345-678',
            'endereco': 'Rua das Flores',
            'numero': 123,
            'bairro': 'Centro',
            'cidade': 'Cubatão',
            'estado': 'SP',
        }
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_formulario_de_perfil_invalido_campos_ausentes(self):
        form_data = {
            'user_id': 1,
            'nome': '',
            'sobrenome': '',
            'email': 'invalidemail',
            'documento': '',
            'contato': '',
            'data_nascimento': '',
            'cep': '',
            'endereco': '',
            'numero': '',
            'bairro': '',
            'cidade': '',
            'estado': '',
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)
        self.assertIn('sobrenome', form.errors)
        self.assertIn('email', form.errors)


class PaymentsFormTests(TestCase):
    def test_formulario_de_pagamentos_validos(self):
        form_data = {
            'cartao_id': '123',
            'nome_titular': 'John Doe',
            'numero_cartao': '0000 0000 0000 0000',
            'validade': '12/25',
            'documento': '12345678909',
            'cvc': '123',
        }
        form = PaymentsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_formulario_de_pagamentos_invalido_campos_ausentes(self):
        form_data = {
            'cartao_id': '',
            'nome_titular': '',
            'numero_cartao': '',
            'validade': '',
            'documento': '',
            'cvc': '',
        }
        form = PaymentsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nome_titular', form.errors)
        self.assertIn('numero_cartao', form.errors)
        self.assertIn('validade', form.errors)
