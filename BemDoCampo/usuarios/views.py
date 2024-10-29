from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.http import Http404
from .imagens import MediaRecords
from . import forms
from django.views import View
from datetime import datetime
from . import models
import uuid

@login_required(login_url='/accounts/login')
def dashboard(request):
    return render(request, 'dashboard.html')

@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
class ProfileView(View):
    template_name = 'pages/profile.html'
    media = MediaRecords()

    def get(self, request):
        try:
            user = models.Usuarios.objects.using('mongo').get(user_id=request.user.id)
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
        
        return render(request, self.template_name, context={'user_data':user_data, 'form': forms.ProfileForm(user_data)})
    
    def session_user(self, request):
        return {
            'nome': request.user.first_name,
            'sobrenome': request.user.last_name,
            'email': request.user.email,
            'user_id': request.user.id,
        }

    def post(self, request):
        form = forms.ProfileForm(request.POST)
        
        user_id = form.data['user_id']

        date_nasc = (
            datetime.strptime(form.data['data_nascimento'], "%d/%m/%Y").strftime("%Y-%m-%d")
            if form.data['data_nascimento'] else None
        )
        
        image_path = self.media.image_path(
            request.FILES.get('imagem_perfil'),
            user_id
        )

        usuario_atualizado = models.Usuarios.objects.using('mongo').filter(user_id=user_id).first()
        
        if usuario_atualizado:
            self.update_usuario(form, usuario_atualizado, date_nasc, image_path)
        else:
            novo_usuario = self.create_usuario(form, user_id, date_nasc, image_path)
            novo_usuario.save(using='mongo')

        return redirect('dashboard')

    def update_usuario(self, form, usuario, date_nasc, image_path):
        novos_dados = {
            'nome': form.data.get('nome', usuario.nome),
            'sobrenome': form.data.get('sobrenome', usuario.sobrenome),
            'email': form.data.get('email', usuario.email),
            'documento': form.data.get('documento', usuario.documento),
            'contato': form.data.get('contato', usuario.contato),
            'data_nascimento': date_nasc or usuario.data_nascimento,
            'cep': form.data.get('cep', usuario.cep),
            'endereco': form.data.get('endereco', usuario.endereco),
            'numero': form.data.get('numero', usuario.numero),
            'bairro': form.data.get('bairro', usuario.bairro),
            'cidade': form.data.get('cidade', usuario.cidade),
            'estado': form.data.get('estado', usuario.estado),
            'imagem_perfil': image_path or usuario.imagem_perfil,
        }

        models.Usuarios.objects.using('mongo').filter(user_id=usuario.user_id).update(**novos_dados)

    def create_usuario(self, form, user_id, date_nasc, image_path):
        return models.Usuarios(
            user_id=user_id,
            nome=form.data.get('nome', ''),
            sobrenome=form.data.get('sobrenome', ''),
            email=form.data.get('email', ''),
            documento=form.data.get('documento', ''),
            contato=form.data.get('contato', ''),
            data_nascimento=date_nasc,
            cep=form.data.get('cep', ''),
            endereco=form.data.get('endereco', ''),
            numero=form.data.get('numero', ''),
            bairro=form.data.get('bairro', ''),
            cidade=form.data.get('cidade', ''),
            estado=form.data.get('estado', ''),
            imagem_perfil=image_path or "/NoPhotoUser.png",
        )

@login_required(login_url='/accounts/login')
def payment(request):
    return render(request, 'pages/payment.html')    

class ProductsView(View):
    template_name = 'pages/stock.html'
    
    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
class PaymentViews(View):
    template_name = "pages/payment.html"
    
    def get(self, request):
        payments = models.FormaPagamento.objects.using('mongo').all()  # Buscando todos os cartões
        context = {
            "form": forms.PaymentsForm(),
            "payments": payments
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = forms.PaymentsForm(request.POST)
        
        if form.is_valid():
            
            user_id = request.user.id
            novo_pagamento = form.save(commit=False)
            novo_pagamento.id_cartao = str(uuid.uuid4())  # Gerar UUID
            novo_pagamento.user_id = user_id
            novo_pagamento.save(using='mongo')            
            return redirect('payment')
        
        payments = models.FormaPagamento.objects.using('mongo').all()
        context = {
            "form": form,
            "payments": payments
        }
        return render(request, self.template_name, context=context)
        
    def update_pagamento(self, form, pagamento):
        novos_dados = {
            'id_cartao': uuid.uuid4,
            'nome_titular': form.data.get('nome_titular', pagamento.cartoes.nome_titular),
            'numero_cartao': form.data.get('numero_cartao', pagamento.cartoes.numero_cartao),
            'validade': form.data.get('validade', pagamento.cartoes.validade),
            'documento': form.data.get('documento', pagamento.cartoes.documento),
            'cvc': form.data.get('cvc', pagamento.cartoes.cvc)
        }
        models.Usuarios.objects.using('mongo').filter(user_id=pagamento.user_id).update()

@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
class PaymentEditView(View):
    template_name = "pages/payment_edit.html"  
    
    def get_payment_or_404(self, pk):
        pagamento = models.FormaPagamento.objects.using('mongo').filter(id_cartao=pk).first()  
        if not pagamento:
            raise Http404("Cartão não encontrado")
        return pagamento
    
    def get(self, request, pk):
        pagamento = self.get_payment_or_404(pk)  
        form = forms.PaymentsForm(instance=pagamento)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        pagamento = self.get_payment_or_404(pk)  
        form = forms.PaymentsForm(request.POST, instance=pagamento)  # Atualiza com os dados do cartão
        
        if form.is_valid():
            form.save(commit=False)
            pagamento.save(using='mongo')
            return redirect('payment')
        
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
class PaymentDeleteView(View):
    def post(self, request, pk):
        pagamento = models.FormaPagamento.objects.using('mongo').filter(id_cartao=pk).first()
        if pagamento:
            pagamento.delete()  # Exclui o cartão
        return redirect('payment')        
