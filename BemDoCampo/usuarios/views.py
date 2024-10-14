from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import View
from datetime import datetime
from .models import Usuarios

@login_required(login_url='/accounts/login')
def dashboard(request):
    return render(request, 'dashboard.html')

@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
class ProfileView(View):
    template_name = 'pages/profile.html'

    def get(self, request):
        try:
            user = Usuarios.objects.using('mongo').get(user_id=request.user.id)
            context = self.session_user(request)
            context.update({
                'document': user.documento,
                'contact': user.contato,
                'dt_nasc': f"{user.data_nascimento:%d/%m/%Y}",
                'cep': user.cep,
                'endereco': user.endereco,
                'number': user.numero,
                'bairro': user.bairro,
                'cidade': user.cidade,
                'estado': user.estado,
            })
        except:
            context = self.session_user(request)
        return render(request, self.template_name, context)
    
    def session_user(self, request):
        return {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'user_id': request.user.id,
        }

    def post(self, request):
        user_id = request.POST.get('user_id')

        date_nasc = (
            datetime.strptime(request.POST.get('data_nascimento'), "%d/%m/%Y").strftime("%Y-%m-%d")
            if request.POST.get('data_nascimento') else None
        )

        usuario_atualizado = Usuarios.objects.using('mongo').filter(user_id=user_id).first()
        
        if usuario_atualizado:
            self.update_usuario(request, usuario_atualizado, date_nasc)
        else:
            novo_usuario = self.create_usuario(request, user_id, date_nasc)
            novo_usuario.save(using='mongo')

        return redirect('dashboard')

    def update_usuario(self, request, usuario, date_nasc):
        novos_dados = {
            'nome': request.POST.get('nome', usuario.nome),
            'sobrenome': request.POST.get('sobrenome', usuario.sobrenome),
            'email': request.POST.get('email', usuario.email),
            'documento': request.POST.get('documento', usuario.documento),
            'contato': request.POST.get('contato', usuario.contato),
            'data_nascimento': date_nasc or usuario.data_nascimento,
            'cep': request.POST.get('cep', usuario.cep),
            'endereco': request.POST.get('endereco', usuario.endereco),
            'numero': request.POST.get('numero', usuario.numero),
            'bairro': request.POST.get('bairro', usuario.bairro),
            'cidade': request.POST.get('cidade', usuario.cidade),
            'estado': request.POST.get('estado', usuario.estado),
        }

        Usuarios.objects.using('mongo').filter(user_id=usuario.user_id).update(**novos_dados)

    def create_usuario(self, request, user_id, date_nasc):
        # Cria um novo usuário
        return Usuarios(
            user_id=user_id,
            nome=request.POST.get('nome', ''),
            sobrenome=request.POST.get('sobrenome', ''),
            email=request.POST.get('email', ''),
            documento=request.POST.get('documento', ''),
            contato=request.POST.get('contato', ''),
            data_nascimento=date_nasc,
            cep=request.POST.get('cep', ''),
            endereco=request.POST.get('endereco', ''),
            numero=request.POST.get('numero', ''),
            bairro=request.POST.get('bairro', ''),
            cidade=request.POST.get('cidade', ''),
            estado=request.POST.get('estado', ''),
        )


@login_required(login_url='/accounts/login')
def payment(request):
    return render(request, 'pages/payment.html')