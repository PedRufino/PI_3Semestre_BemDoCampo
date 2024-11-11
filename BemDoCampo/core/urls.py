from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('sobre/', views.SobreView.as_view(), name='sobre'),
    path('contato/', views.ContatoView.as_view(), name='contato'),
]
