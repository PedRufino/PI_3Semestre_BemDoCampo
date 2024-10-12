from django.shortcuts import render, redirect
from .models import Localizacao, Alimento
from datetime import datetime

def hello_word(request):
    return render(request, 'index.html')

def adicionar_alimento(request):
    if request.method == 'POST':
        localizacao = Localizacao(cidade=request.POST['cidade'], estado=request.POST['estado'])
        localizacao.save()

        novo_alimento = Alimento(
            alimento_id=request.POST['alimento_id'],
            nome=request.POST['nome'],
            tipo=request.POST['tipo'],
            quantidade=int(request.POST['quantidade']),
            unidade=request.POST['unidade'],
            descricao=request.POST['descricao'],
            produtor_id=request.POST['produtor_id'],
            localizacao=localizacao.to_mongo(),  
            imagem_capa=request.POST['imagem_capa'],
            imagens=request.POST.getlist('imagens'),
            data_cadastro=datetime.utcnow(),
        )
        novo_alimento.save()
        return redirect('hello_world')
    
    return render(request, 'adicionar.html')