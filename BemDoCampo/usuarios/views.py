from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import (
    redirect,
    render
)

from .imagens import MediaRecords
from django.views import View
from . import models
from . import forms
import uuid

@login_required(login_url='/accounts/login')
def dashboard(request):
    return render(request, 'dashboard.html')

@method_decorator(login_required(), name='dispatch')
class ProfileView(View):
    template_name = 'pages/profile.html'
    media = MediaRecords()

    def get(self, request):
        paths = request.path.strip('/').split('/')
        
        try:
            user = models.Usuarios.objects(user_id=request.user.id).first()
            
            user_data = self.session_user(request)
            user_data.update({
                'documento': user.documento,
                'contato': user.contato,
                'data_nascimento': f"{user.data_nascimento:%d/%m/%Y}",
                'cep': user.cep,
                'endereco': user.endereco,
                'numero': user.numero,
                'bairro': user.bairro,
                'cidade': user.cidade,
                'estado': user.estado,
                'imagem_perfil': user.imagem_perfil
            })
        except:
            user_data = self.session_user(request)

        return render(request, self.template_name, context={'user_data': user_data, 'paths':paths, 'form': forms.ProfileForm(user_data)})
    
    def session_user(self, request):
        return {
            'nome': request.user.first_name,
            'sobrenome': request.user.last_name,
            'email': request.user.email,
            'user_id': request.user.id,
        }

    def post(self, request):
        form = forms.ProfileForm(request.POST)
        
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            
            image_path = self.media.image_path(
                request.FILES.get('imagem_perfil'),
                user_id
            )

            usuario_atualizado = models.Usuarios.objects(user_id=user_id).first()
            
            if usuario_atualizado:
                self.update_usuario(form, usuario_atualizado, image_path)
            else:
                novo_usuario = self.create_usuario(form, user_id, image_path)
                novo_usuario.save(using='mongo')

            return redirect('dashboard')

        return render(request, self.template_name)

    def update_usuario(self, form, usuario, image_path):
        novos_dados = {
            'nome': form.cleaned_data.get('nome', usuario.nome),
            'sobrenome': form.cleaned_data.get('sobrenome', usuario.sobrenome),
            'email': form.cleaned_data.get('email', usuario.email),
            'documento': form.cleaned_data.get('documento', usuario.documento),
            'contato': form.cleaned_data.get('contato', usuario.contato),
            'data_nascimento': form.cleaned_data.get('data_nascimento', usuario.data_nascimento),
            'cep': form.cleaned_data.get('cep', usuario.cep),
            'endereco': form.cleaned_data.get('endereco', usuario.endereco),
            'numero': form.cleaned_data.get('numero', usuario.numero),
            'bairro': form.cleaned_data.get('bairro', usuario.bairro),
            'cidade': form.cleaned_data.get('cidade', usuario.cidade),
            'estado': form.cleaned_data.get('estado', usuario.estado),
            'imagem_perfil': image_path or usuario.imagem_perfil,
        }

        models.Usuarios.objects(user_id=usuario.user_id).update(**novos_dados)

    def create_usuario(self, form, user_id, image_path):
        return models.Usuarios(
            user_id=user_id,
            nome=form.cleaned_data.get('nome', ''),
            sobrenome=form.cleaned_data.get('sobrenome', ''),
            email=form.cleaned_data.get('email', ''),
            documento=form.cleaned_data.get('documento', ''),
            contato=form.cleaned_data.get('contato', ''),
            data_nascimento=form.cleaned_data.get('data_nascimento', ''),
            cep=form.cleaned_data.get('cep', ''),
            endereco=form.cleaned_data.get('endereco', ''),
            numero=form.cleaned_data.get('numero', ''),
            bairro=form.cleaned_data.get('bairro', ''),
            cidade=form.cleaned_data.get('cidade', ''),
            estado=form.cleaned_data.get('estado', ''),
            imagem_perfil=image_path or "/NoPhotoUser.png",
        )

@method_decorator(login_required(), name='dispatch')
class PaymentViews(View):
    template_name = "pages/payment.html"
    
    def get(self, request):
        user_id = request.user.id
        try:
            usuario = models.Usuarios.objects.get(user_id=user_id)
            payments = usuario.formas_pagamento
        except models.Usuarios.DoesNotExist:
            payments = []
        
        context = {
            "form": forms.PaymentsForm(),
            "payments": payments
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = forms.PaymentsForm(request.POST)
        
        if form.is_valid():
            cartao_id = form.cleaned_data.get('cartao_id', None)
            user_id = request.user.id
            try:
                usuario = models.Usuarios.objects.get(user_id=user_id)
                if cartao_id:
                    self.update_payment(usuario, form, cartao_id)
                else:
                    self.create_payment(usuario, form)
                
                return redirect('payment')
                
            except models.Usuarios.DoesNotExist:
                return redirect('some_error_page')
        
        return render(request, self.template_name)

    def update_payment(self, usuario, form, cartao_id):
        forma_pagamento = next((fp for fp in usuario.formas_pagamento if fp.id_cartao == cartao_id), None)
        if forma_pagamento:
            forma_pagamento.nome_titular = form.cleaned_data.get('nome_titular', forma_pagamento.nome_titular)
            forma_pagamento.numero_cartao = form.cleaned_data.get('numero_cartao', forma_pagamento.numero_cartao)
            forma_pagamento.validade = form.cleaned_data.get('validade', forma_pagamento.validade)
            forma_pagamento.documento = form.cleaned_data.get('documento', forma_pagamento.documento)
            forma_pagamento.cvc = form.cleaned_data.get('cvc', forma_pagamento.cvc)
            usuario.save(using='mongo')

    def create_payment(self, usuario, form):
        nova_forma_pagamento = models.FormaPagamento(
            id_cartao=str(uuid.uuid4()),
            nome_titular=form.cleaned_data['nome_titular'],
            numero_cartao=form.cleaned_data['numero_cartao'],
            validade=form.cleaned_data['validade'],
            documento=form.cleaned_data['documento'],
            cvc=form.cleaned_data['cvc']
        )
        
        usuario.formas_pagamento.append(nova_forma_pagamento)
        usuario.save(using='mongo')

@method_decorator(login_required(), name='dispatch')
class PaymentDeleteView(View):
    def post(self, request, pk):
        user_id = request.user.id
        
        try:
            usuario = models.Usuarios.objects.get(user_id=user_id)

            forma_pagamento = next((fp for fp in usuario.formas_pagamento if fp.id_cartao == pk), None)

            if forma_pagamento:
                usuario.formas_pagamento.remove(forma_pagamento)
                usuario.save(using='mongo')

        except models.Usuarios.DoesNotExist:
            pass

        return redirect('payment')
