from django.urls import path
from . import views

urlpatterns = [
    path('estoque/', views.StockView.as_view(), name='stock'),
    path('estoque/atualizar/<str:produto_id>', views.ProductsView.as_view(), name='edit_product'),
    path('estoque/excluir/<str:produto_id>', views.StockView.as_view(), name='delete_product'),
    path('cadastro/', views.ProductsView.as_view(), name='products'),
]
