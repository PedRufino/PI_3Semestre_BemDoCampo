from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('payment/', views.PaymentViews.as_view(), name='payment'),
    path('stock/', views.ProductsView.as_view(), name='stock'),
    path('perfil/', views.ProfileView.as_view(), name='profile'),
    path('perfil/imagem', views.ProfileView.as_view(), name='imagem'),
    path('payment/delete/<str:pk>/', views.PaymentDeleteView.as_view(), name='payment_delete'),
    path('payment/edit/<str:pk>/', views.PaymentEditView.as_view(), name='payment_edit')
]
