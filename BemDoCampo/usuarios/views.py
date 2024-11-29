from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import (
    redirect,
    render
)

from .imagens import MediaRecords
from django.views import View
from random import randint
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
        try:
            user = models.Usuarios.objects(user_id=request.user.id).first()
            
            user_data = self.session_user(request)
            user_data.update({
                'documento': user.documento,
                'tipo_usuario': user.tipo_usuario,
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
        except Exception as e:
            user_data = self.session_user(request)
        
        context = {
            'user_data': user_data, 
            'paths':['Configurações', 'Conta'], 
            'form': forms.ProfileForm(user_data)
        }

        return render(request, self.template_name, context=context)
    
    def session_user(self, request):
        social_account = request.user.socialaccount_set.filter(provider='google').first()
        profile_picture = (
            social_account.extra_data.get('picture') if social_account else None
        )

        return {
            'nome': request.user.first_name,
            'sobrenome': request.user.last_name,
            'email': request.user.email,
            'user_id': request.user.id,
            'imagem_google': profile_picture
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
            
            number = [randint(5, 95), randint(5, 95)]
            tmp_entrega = {"min": min(number), "max": max(number)}
            
            if usuario_atualizado:
                self.update_usuario(form, usuario_atualizado, image_path, tmp_entrega)
            else:
                novo_usuario = self.create_usuario(form, user_id, image_path, tmp_entrega)
                novo_usuario.save(using='mongo')

            return redirect('dashboard')

        return render(request, self.template_name)

    def update_usuario(self, form, usuario, image_path, tmp_entrega):
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

    def create_usuario(self, form, user_id, image_path, tmp_entrega):
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
            'paths':['Configurações', 'Pagamento'], 
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


@method_decorator(login_required(), name="dispatch")
class MyTendaView(View):
    template_name = 'pages/my_tenda.html'
    media = MediaRecords()

    def get(self, request):        
        try:
            user = models.Usuarios.objects(user_id=request.user.id).first()
            
            minha_tenda = user.minha_tenda if user and user.minha_tenda else {}
            
            minha_tenda={
                "id_tenda": minha_tenda.id_tenda,
                "nome_tenda": minha_tenda.nome_tenda,
                "tipo_usuario": user.tipo_usuario,
                "email": minha_tenda.email,
                "documento": minha_tenda.documento,
                "contato": minha_tenda.contato,
                "cep": minha_tenda.cep,
                "endereco": minha_tenda.endereco,
                "numero": minha_tenda.numero,
                "bairro": minha_tenda.bairro,
                "cidade": minha_tenda.cidade,
                "estado": minha_tenda.estado,
                "imagem_tenda": minha_tenda.imagem_tenda,
                "tx_entrega": minha_tenda.tx_entrega,
                "tempo_entrega": minha_tenda.tempo_entrega,
                "avaliacoes_estrelas": minha_tenda.avaliacoes_estrelas,
                "media_avaliacoes": minha_tenda.media_avaliacoes
            }
        except Exception as e:
            minha_tenda = {}
        
        context = {
            'minha_tenda': minha_tenda, 
            'paths': ['Configurações', 'Minha Tenda'], 
            'form': forms.MyTendaForm(minha_tenda)
        }

        return render(request, self.template_name, context=context)
    
    def post(self, request):
        form = forms.MyTendaForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.user.id
            user = models.Usuarios.objects(user_id=user_id).first()
            id_tenda = str(uuid.uuid4())
            
            if not user:
                return redirect('dashboard')

            minha_tenda_data = user.minha_tenda.to_mongo() if user.minha_tenda else {}
            minha_tenda = self.update_or_create_tenda(form, minha_tenda_data, request.FILES.get('imagem_tenda'), user_id, id_tenda)
            
            user.minha_tenda = minha_tenda
            user.save()

            return redirect('dashboard')

        return render(request, self.template_name, {'form': form})


    def update_or_create_tenda(self, form, tenda_data, image, user_id, id_tenda):        
        id_tenda = tenda_data.get('id_tenda', id_tenda)
        
        if tenda_data.get('image_tenda', None):
            self.delete_image(tenda_data.get('image_tenda', None))
        
        image_path = self.media.image_path(
            image,
            user_id,
            tenda_data.get('id_tenda', id_tenda)
        )
        
        return models.MinhaTenda(
            id_tenda=id_tenda,
            nome_tenda=form.cleaned_data.get('nome_tenda', ''),
            tx_entrega=form.cleaned_data.get('tx_entrega', 0.0),
            tempo_entrega=self.generate_delivery_time(),
            email=form.cleaned_data.get('email', ''),
            documento=form.cleaned_data.get('documento', ''),
            contato=form.cleaned_data.get('contato', ''),
            cep=form.cleaned_data.get('cep', ''),
            endereco=form.cleaned_data.get('endereco', ''),
            numero=form.cleaned_data.get('numero', 0),
            bairro=form.cleaned_data.get('bairro', ''),
            cidade=form.cleaned_data.get('cidade', ''),
            estado=form.cleaned_data.get('estado', ''),
            imagem_tenda=tenda_data.get('image_tenda', image_path),
        )


    def generate_delivery_time(self):
        numbers = [randint(5, 95), randint(5, 95)]
        return {"min": min(numbers), "max": max(numbers)}