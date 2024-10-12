from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_word, name='hello_world'),
    path('adicionar_alimento/', views.adicionar_alimento, name='adicionar_alimento'),
    
]
