from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import View

class IndexView(View):
    template_name = 'index.html'
    color_product = '#000000'
    
    def get(self, request):
        context = {
            'tipos_produtos': {
                'fruta': {'nome':'Fruta', 'class': "fa-apple-whole", "color": f'{self.color_product}'},
                'verdura': {'nome':'Verdura', 'class': "fa-solid fa-carrot", "color": f'{self.color_product}'},
                'grao': {'nome':'Grão', 'class': "fa-wheat-awn", "color": f'{self.color_product}'},
                'laticinio': {'nome':'Laticínio', 'class': "fa-cow", "color": f'{self.color_product}'},
                'carne': {'nome':'Carne', 'class': "fa-drumstick-bite", "color": f'{self.color_product}'},
                'peixe': {'nome':'Peixe', 'class': "fa-fish", "color": f'{self.color_product}'},
                'cereal': {'nome':'Cereal', 'class': "fa-wheat-awn", "color": f'{self.color_product}'},
                'temperos': {'nome':'Temperos', 'class': "fa-leaf", "color": f'{self.color_product}'},
                'oleo': {'nome':'Óleo', 'class': "fa-bottle-droplet", "color": f'{self.color_product}'},
                'bebida': {'nome':'Bebida', 'class': "fa-wine-bottle", "color": f'{self.color_product}'},
                'doces': {'nome':'Doces', 'class': "fa-candy-cane", "color": f'{self.color_product}'},
            }
        }
        return render(request, self.template_name, context=context)