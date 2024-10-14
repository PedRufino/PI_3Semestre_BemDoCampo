from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('payment/', views.payment, name='payment')
]
