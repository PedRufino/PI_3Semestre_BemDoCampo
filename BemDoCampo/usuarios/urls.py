from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('payment/', views.PaymentViews.as_view(), name='payment'),
    path('perfil/', views.ProfileView.as_view(), name='profile'),
    path('perfil/minha_tenda', views.MyTendaView.as_view(), name='my_tenda'),
    path('perfil/imagem', views.ProfileView.as_view(), name='imagem'),
    path('payment/delete/<str:pk>/', views.PaymentDeleteView.as_view(), name='payment_delete')
]
