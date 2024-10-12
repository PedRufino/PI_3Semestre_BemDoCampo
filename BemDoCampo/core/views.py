from django.shortcuts import render, redirect
from .models import Produtos

def hello_word(request):
    return render(request, 'index.html')

def adicionar_produtos(request):
    if request.method == 'POST':
        # Criar um novo alimento
        novo_produto = Produtos(
            nome=request.POST['nome'],
            tipo=request.POST['tipo'],
            quantidade=int(request.POST['quantidade']),
            unidade=request.POST['unidade'],
            descricao=request.POST['descricao'],
            produtor_id=request.POST['produtor_id'],
            imagem_capa=request.POST['imagem_capa'],
            imagens=request.POST.getlist('imagens'),
            
        )
        
        # Salvar o alimento no MongoDB
        novo_produto.save(using='mongo')

        # Redirecionar para a página de boas-vindas
        return redirect('hello_world')
    
    return render(request, 'adicionar.html')
