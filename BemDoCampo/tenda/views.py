from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import mongoengine


# db = mongoengine.connection.get_db()
# self.db.produtos.find()

class TendaView(View):
    template_name = 'tenda.html'
    db = mongoengine.connection.get_db()

    def get(self, request, produtor_id):
        context = {
            'produtos': self.produtos(produtor_id),
            'produtor': self.produtor(produtor_id)[0],
            'paths':  ['Tenda', self.produtor(produtor_id)[0]['nome']]
        }
        
        print(context)
        
        return render(request, self.template_name, context)
    
    def produtos(self, produtor_id):
        produtos = list(self.db.produtos.find({'produtor_id': produtor_id}))
        
        for produto in produtos:
            del produto['_id']

        return produtos
    
    def produtor(self, produtor_id):
        produtor = list(self.db.usuarios.find({'user_id': produtor_id}))
        
        for user in produtor:
            del user['_id']
            
        return produtor
