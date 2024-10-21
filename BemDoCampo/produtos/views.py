from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import (
    redirect,
    render
)

from django.conf import settings
from django.views import View
from . import models
from . import forms
import uuid
import os


@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
class ProductsView(View):
    template_name = 'products.html'
    
    def get(self, request, produto_id=None):
        product=None

        if produto_id:
            product = models.Produtos.objects.using('mongo').get(produto_id=produto_id)
            product.valor = str(product.valor).replace(".", ",")
        
        context = {
            'form': forms.ProductForm(instance=product)
        }

        return render(request, self.template_name, context=context)
    
    def post(self, request):
        form = forms.ProductForm(request.POST)
        
        user_id = request.user.id
        produto_id = form.data.get('produto_id', '')
        valor = float(form.data.get('valor', 0.00).replace('.','').replace(',','.'))
        
        if produto_id:
            produto_atualizado = models.Produtos.objects.using('mongo').filter(produto_id=produto_id).first()
            self.update_produto(request, form, produto_atualizado, produto_id, valor)
        else:
            novo_produto = self.cadastar_produto(request, form, user_id, valor)
            novo_produto.save(using='mongo')

        return redirect('stock')
    
    def update_produto(self, request, form, produto, produto_id, valor):
        request.FILES.get('imagem_capa')
        
        novos_dados = {
            'produto_id': produto_id or produto.produto_id,
            'produtor_id': form.data.get('produtor_id', produto.produtor_id),
            'nome': form.data.get('nome', produto.nome),
            'tipo_produto': form.data.get('tipo_produto', produto.tipo_produto),
            'quantidade': form.data.get('quantidade', produto.quantidade),
            'tipo_unidade': form.data.get('tipo_unidade',produto.tipo_unidade),
            'valor': valor or produto.valor,
            'descricao': form.data.get('descricao',produto.descricao)
        }
        
        nova_imagem = request.FILES.get('imagem_capa')
        if nova_imagem:
            novos_dados['imagem_capa'] = self.caminho_imagem(nova_imagem, produto_id, request.user.id)
        
        models.Produtos.objects.using('mongo').filter(produto_id=produto_id).update(**novos_dados)
    
    def caminho_imagem(self, imagem, produto_id, user_id):
        if not imagem:
            return "/NoPhoto.jpg"
        
        extensao = imagem.name.split('.')[-1]
        nome_arquivo = f"{produto_id}.{extensao}"

        caminho_imagem = os.path.join(settings.MEDIA_ROOT, str(user_id), "prod_img", nome_arquivo)

        os.makedirs(os.path.dirname(caminho_imagem), exist_ok=True)

        with open(caminho_imagem, 'wb+') as destination:
            for chunk in imagem.chunks():
                destination.write(chunk)
        
        return f"{user_id}/prod_img/{nome_arquivo}"

    def cadastar_produto(self, request, form, user_id, valor):
        produto_id = uuid.uuid4()
        caminho = self.caminho_imagem(
            request.FILES.get('imagem_capa'),
            produto_id,
            user_id
        )
        
        return models.Produtos(
            produto_id=produto_id,
            produtor_id=user_id,
            nome=form.data.get('nome',''),
            tipo_produto=form.data.get('tipo_produto',''),
            quantidade=form.data.get('quantidade',''),
            tipo_unidade=form.data.get('tipo_unidade',''),
            valor=valor,
            descricao=form.data.get('descricao',''),
            imagem_capa=caminho,
        )
    

@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
class StockView(View):
    template_name = 'stock.html'
    
    def get(self, request, produto_id=None):
        
        if produto_id:
            produto = models.Produtos.objects.using('mongo').filter(produto_id=produto_id)
            self.delete_imagem(produto.first())
            produto.delete()
            redirect('stock')
        
        produtos = models.Produtos.objects.using('mongo').filter(produtor_id=request.user.id)
        
        context = {
            'produtos': produtos
        }
        
        return render(request, self.template_name, context=context)
    
    def delete_imagem(self, produto):
        try:
            if produto.imagem_capa:
                image_path = os.path.join(settings.MEDIA_ROOT, produto.imagem_capa.path)
                if os.path.exists(image_path):
                    os.remove(image_path)
        except Exception as e:
            print(f"Erro ao deletar a imagem: {e}")