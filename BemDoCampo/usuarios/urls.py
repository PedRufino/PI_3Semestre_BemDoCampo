from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('pagamentos/', views.payment, name='payment'),
    path('perfil/', views.ProfileView.as_view(), name='profile'),
    path('perfil/imagem', views.ProfileView.as_view(), name='imagem'),
]
