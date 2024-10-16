from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('payment/', views.payment, name='payment'),
    path('stock/', views.ProductsView.as_view(), name='stock'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
