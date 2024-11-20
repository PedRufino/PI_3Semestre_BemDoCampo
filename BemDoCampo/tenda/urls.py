from django.urls import path
from . import views

urlpatterns = [
    path('<int:produtor_id>/', views.TendaView.as_view(), name='tenda'), 
]