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
import locale
import uuid

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

@method_decorator(login_required, name='dispatch')
class ProductsView(View):
    template_name = 'products.html'
    media = MediaRecords()

    def get(self, request, produto_id=None):
        product = None

        if produto_id:
            try:
                product = models.Produtos.objects.get(produto_id=produto_id)
                product = {
                    "produto_id": product.produto_id,
                    "nome": product.nome,
                    "tipo_produto": product.tipo_produto,
                    "quantidade": product.quantidade,
                    "tipo_unidade": product.tipo_unidade,
                    "descricao": product.descricao,
                    "produtor_id": product.produtor_id,
                    "valor": str(product.valor).replace('.',',')
                } 
            except models.Produtos.DoesNotExist:
                product = None

        context = {
            'form': forms.ProductForm(product)
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        form = forms.ProductForm(request.POST)
        if form.is_valid():
            user_id = request.user.id
            produto_id = form.cleaned_data.get('produto_id', None)
            
            if produto_id:
                try:
                    produto_atualizado = models.Produtos.objects.get(produto_id=produto_id)
                    self.update_produto(request, form, produto_atualizado, produto_id)
                except models.Produtos.DoesNotExist:
                    return render(request, self.template_name, {'form': form, 'error': 'Produto não encontrado.'})
            else:
                novo_produto = self.cadastrar_produto(request, form, user_id)
                novo_produto.save()

            return redirect('stock')
        return render(request, self.template_name, {'form': form})

    def update_produto(self, request, form, produto, produto_id):
        novos_dados = {
            'produto_id': produto_id,
            'produtor_id': form.cleaned_data.get('produtor_id', produto.produtor_id),
            'nome': form.cleaned_data.get('nome', produto.nome),
            'tipo_produto': form.cleaned_data.get('tipo_produto', produto.tipo_produto),
            'quantidade': form.cleaned_data.get('quantidade', produto.quantidade),
            'tipo_unidade': form.cleaned_data.get('tipo_unidade', produto.tipo_unidade),
            'valor': form.cleaned_data.get('valor', produto.valor),
            'descricao': form.cleaned_data.get('descricao', produto.descricao)
        }
        
        nova_imagem = request.FILES.get('imagem_capa')
        if nova_imagem:
            novos_dados['imagem_capa'] = self.media.image_path(nova_imagem, produto_id, request.user.id)
        
        for key, value in novos_dados.items():
            setattr(produto, key, value)

        produto.save()

    def cadastrar_produto(self, request, form, user_id):
        produto_id = str(uuid.uuid4())
        caminho = self.media.image_path(
            request.FILES.get('imagem_capa'),
            produto_id,
            user_id
        )
        
        return models.Produtos(
            produto_id=produto_id,
            produtor_id=user_id,
            nome=form.cleaned_data.get('nome', ''),
            tipo_produto=form.cleaned_data.get('tipo_produto', ''),
            quantidade=form.cleaned_data.get('quantidade', ''),
            tipo_unidade=form.cleaned_data.get('tipo_unidade', ''),
            valor=form.cleaned_data.get('valor', 0.00),
            descricao=form.cleaned_data.get('descricao', ''),
            imagem_capa=caminho,
        )

@method_decorator(login_required, name='dispatch')
class StockView(View):
    template_name = 'stock.html'
    media = MediaRecords()

    def get(self, request, produto_id=None):
        if produto_id:
            try:
                produto = models.Produtos.objects.get(produto_id=produto_id)
                self.media.delete_image(produto.imagem_capa)
                produto.delete()
            except models.Produtos.DoesNotExist:
                pass

            return redirect('stock')

        produtos = models.Produtos.objects.filter(produtor_id=request.user.id)
        context = {
            'produtos': produtos
        }
        
        return render(request, self.template_name, context=context)
