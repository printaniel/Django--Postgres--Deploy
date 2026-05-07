from django.urls import path
from .views import *

urlpatterns = [
    
    path('productos/',producto_lista_api, name = 'lista_productos'),
    path('disponibles/',productos_disponibles_api, name = 'lista_productos_disponibles'),
    path('pedidos/',pedidos_lista_api, name = 'lista_pedidos'),
    path('pedidos/hoy/', pedido_de_hoy_api, name= 'lista_pedidos_hoy'),
    path('pedidos/resumen/hoy', resumen_pedidos_hoy, name= 'resumen_pedidos_hoy'),
    path('stock_bajo/', productos_stock_bajo, name = 'productos_stock_bajo'),
    path('inventario/' ,inventario, name = 'inventario'),
    path('resumen_pedidos/', resumen_pedidos_personalizados, name = "resumen_pedidos_personalizados")
    ]
