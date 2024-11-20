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
        produtos = list(self.db.produtos.find({'produtor_id': produtor_id}))
        
        for produto in produtos:
            del produto['_id']
        
        context = {
            'produtos': produtos
        }
        
        return render(request, self.template_name, context)



