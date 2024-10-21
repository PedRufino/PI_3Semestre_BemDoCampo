from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_word, name='hello_world'),
    # path('adicionar_produtos/', views.adicionar_produtos, name='adicionar_produtos'),
    
]
