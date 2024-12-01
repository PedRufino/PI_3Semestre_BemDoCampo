from django.shortcuts import render
from django.views import View

class CarrinhoView(View):
    template_name = 'carrinho.html'
    def get(self, request):
        produtos = []
        total = 0
        for x in range(1, 11):
            produtos.append({
                'nome': f'Produto {x}',
                'tipo': f'Tipo {x}',
                'quantidade': x,
                'preco': x,
                'unidade_medida': f'uni {x}'
            })
            
            total += x
        
        context = {
            'items': {
                'produtos': produtos,
                'total': total,
                'quantidade': len(produtos)
            }
        }
        
        print(context)
        
        return render(request, self.template_name, context=context)
