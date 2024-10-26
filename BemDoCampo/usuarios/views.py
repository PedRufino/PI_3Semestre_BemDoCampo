from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from .imagens import MediaRecords
from .forms import ProfileForm
from django.views import View
from datetime import datetime
from .models import Usuarios

@login_required(login_url='/accounts/login')
def dashboard(request):
    return render(request, 'dashboard.html')

@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
class ProfileView(View):
    template_name = 'pages/profile.html'
    media = MediaRecords()

    def get(self, request):
        try:
            user = Usuarios.objects.using('mongo').get(user_id=request.user.id)
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
        
        return render(request, self.template_name, context={'user_data':user_data, 'form': ProfileForm(user_data)})
    
    def session_user(self, request):
        return {
            'nome': request.user.first_name,
            'sobrenome': request.user.last_name,
            'email': request.user.email,
            'user_id': request.user.id,
        }

    def post(self, request):
        form = ProfileForm(request.POST)
        
        user_id = form.data['user_id']

        date_nasc = (
            datetime.strptime(form.data['data_nascimento'], "%d/%m/%Y").strftime("%Y-%m-%d")
            if form.data['data_nascimento'] else None
        )
        
        image_path = self.media.image_path(
            request.FILES.get('imagem_perfil'),
            user_id
        )

        usuario_atualizado = Usuarios.objects.using('mongo').filter(user_id=user_id).first()
        
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

        Usuarios.objects.using('mongo').filter(user_id=usuario.user_id).update(**novos_dados)

    def create_usuario(self, form, user_id, date_nasc, image_path):
        return Usuarios(
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