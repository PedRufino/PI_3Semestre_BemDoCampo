from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View
import mongoengine
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class IndexView(View):
    template_name = 'index.html'
    db = mongoengine.connection.get_db()
    
    def get(self, request):
        context = {
            'produtos': self.favoritos_momento(),
            'paths': ['Bem do Campo', 'Mercado']
        }
        return render(request, self.template_name, context=context)
    
    def favoritos_momento(self):
        produtos_cursor = self.db.produtos.find().limit(10).sort([('total_vendas', -1)])
        produtos_favoritos = []

        for produto in produtos_cursor:
            user_id = produto['produtor_id']
            usuario = self.db.usuarios.find_one({'user_id': user_id})
            dados = {}

            if usuario:
                if usuario.get('minha_tenda', None):
                    dados = {
                        'tempo_entrega': f"{usuario['minha_tenda'].get('tempo_entrega').get('min')}-{usuario['minha_tenda'].get('tempo_entrega').get('max')}",
                        'media_avaliacoes': usuario['minha_tenda'].get('media_avaliacoes'),
                        'tx_entrega': usuario['minha_tenda'].get('tx_entrega'),
                    }

            produtos_favoritos.append({
                'nome': produto.get('nome'),
                'valor': produto.get('valor'),
                'imagem_capa': produto.get('imagem_capa'),
                'user': dados,
            })
        
        return produtos_favoritos



class SobreView(View):
    template_name = 'pages/sobre.html'
    
    def get(self, request):
        context = {
            'paths': ['Bem do Campo','Sobre Nós']
        }
        return render(request, self.template_name, context=context)

class ContatoView(View):
    template_name = 'pages/contato.html'
    
    def get(self, request):
        context = {
            'paths': ['Bem do Campo','Contato']
        }
        return render(request, self.template_name, context=context)

class TendasListView(View):
    db = mongoengine.connection.get_db()
    
    def get(self, request, page_number=1):
        tendas = list(self.db.usuarios.find({'tipo_usuario': {'$ne': 'consumidor'}}))
        
        if request.GET.get('filtro', False):
            tendas = self.aplicar_filtros(request)
            
        if not tendas:
            return JsonResponse({
                'erro': True,
                'msg': 'Nenhum resultado encontrado'
            })
        
        paginator = Paginator(self.parse_tenda(tendas), 12)

        if page_number > paginator.num_pages:
            items_data = []
        else:
            items_data = [item for item in paginator.get_page(page_number)]

        return JsonResponse({"erro": False, "items": items_data, "pages": paginator.num_pages})
    
    def aplicar_filtros(self, request):
        filtros = {'tipo_usuario': {'$ne': 'consumidor'}}
        orders = []

        if request.GET.get('descAvaliacao', False):
            descAvaliacao = request.GET['descAvaliacao']
            if 'true' in descAvaliacao:
                orders.append(('minha_tenda.media_avaliacoes', -1))
        
        if request.GET.get('tempoEntrega', False):
            tempoEntrega = request.GET['tempoEntrega']
            if 'true' in tempoEntrega:
                orders.append(('minha_tenda.tempo_entrega', 1))
        
        if request.GET.get('taxaEntrega', False):
            taxaEntrega = request.GET['taxaEntrega']
            if 'true' in taxaEntrega:
                orders.append(('minha_tenda.tx_entrega', 1))
        
        if request.GET.get('filterBy', ''):
            filter_by = request.GET['filterBy']
            filtros['tipo_usuario'] = filter_by
        
        if request.GET.get('search', ''):
            search = request.GET['search']
            filtros['minha_tenda.nome_tenda'] = {"$regex": f"^{search}", "$options": "i"}
        
        if request.GET.get('entregaGratis', False):
            entregaGratis = request.GET['entregaGratis']
            if 'true' in entregaGratis:
                filtros['minha_tenda.tx_entrega'] = 0

        query = self.db.usuarios.find(filtros)

        if orders:
            query = query.sort(orders)
        
        return list(query)

    def parse_tenda(self, tendas):
        item = []
        for tenda in tendas:
            if tenda:
                if tenda.get('minha_tenda'):
                    if not tenda['minha_tenda']['tx_entrega']:
                        valor = "Grátis"
                    else:
                        valor = locale.currency(tenda['minha_tenda']['tx_entrega'], grouping=True)
                        
                    item.append({
                        "user_id": tenda['user_id'],
                        "nome_tenda": tenda['minha_tenda']['nome_tenda'].title(),
                        "tx_entrega": valor,
                        "tmp_entrega": tenda['minha_tenda']['tempo_entrega'],
                        "tipo_usuario": tenda['tipo_usuario'].title(),
                        "media_avaliacoes": tenda['minha_tenda']['media_avaliacoes'],
                        "imagem_perfil": tenda['minha_tenda'].get('imagem_tenda', 'NoPhotoUser.png'),
                    })
        return item
