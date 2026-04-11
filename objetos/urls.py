from django.urls import path
from .views import producto_lista_api, productos_disponibles_api

urlpatterns = [
    
    path('',producto_lista_api, name = 'lista_productos'),
    path('disponibles/',productos_disponibles_api, name = 'lista_productos_disponibles')

]