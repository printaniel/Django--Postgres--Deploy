""""""
from django.shortcuts import render
from .models import *
from .serializers import ProductoSerializer, PedidoSerializer, ProductoInventarioSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Sum, Avg, Max, F, DecimalField, ExpressionWrapper, Value
from django.db.models.functions import Coalesce



## Productos ##

@api_view(['GET', 'POST'])
def producto_lista_api(request):
    
    if request.method == 'GET':
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many = True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    
@api_view(['GET'])
def productos_disponibles_api(request):
    
    productos_disponibles = Producto.objects.filter(disponible = True)
    serializer = ProductoSerializer(productos_disponibles, many = True)
        
    return Response(serializer.data)

@api_view(['GET'])
def productos_stock_bajo(request):
    
    productos_stock_bajos = Producto.objects.filter(stock__lte=F('stock_minimo'))
    serializer = ProductoSerializer(productos_stock_bajos, many = True)
    
    return Response(serializer.data)


## Pedidos ##


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def pedidos_lista_api(request):
    
    if request.method == 'GET':
        pedidos = Pedido.objects.all()
        serializer = PedidoSerializer(pedidos, many = True)
        return Response(serializer.data)
    else:
        serializer = PedidoSerializer(data = request.data)

        if serializer.is_valid():
            producto = Producto.objects.filter(id = request.data["producto"]).first()
            
            if producto.stock < request.data["cantidad"]:
                return Response({"error": "Stock insuficiente"}, status = 400)
            else:
                print(f"{producto.nombre}: {producto.stock}")
                producto.stock -= request.data["cantidad"]
                producto.save()
                print(f"{producto.nombre}: {producto.stock}")
                serializer.save()
                return Response(serializer.data, status = 201)
            
        return Response(serializer.errors,status = 400 )
        
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pedido_de_hoy_api(request):
    
    fecha_hoy = timezone.localtime().date()
    pedidos_hoy = Pedido.objects.filter( fecha = fecha_hoy )
    serializers =  PedidoSerializer(pedidos_hoy, many =  True)
    
    return Response(serializers.data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def resumen_pedidos_hoy(request):
    
    fecha_hoy = timezone.localtime().date()
    resumen = {"fecha": fecha_hoy}
    
    resumen.update(Pedido.objects.filter(fecha = fecha_hoy).aggregate(total_pedidos = Count('id'), ingresos_hoy = Coalesce(Sum('total'), Value(0, output_field= DecimalField()))))
    
    productos_contados = Pedido.objects.values("producto__id",'producto__nombre').annotate(
    veces_vendido=Count('producto')).order_by('-veces_vendido')
    producto_mas_vendido = productos_contados.first()
    resumen['producto_mas_vendido'] = producto_mas_vendido['producto__nombre']
    
    resumen['productos_con_stock_bajo'] = Producto.objects.filter(stock__lte = F('stock_minimo')).count()
    resumen.update(Producto.objects.aggregate(valor_total_inventario = Sum(ExpressionWrapper(F('stock') * F('precio'),
                                                                             output_field = DecimalField(max_digits = 12, decimal_places = 2))))
    )
    return Response(resumen)

@api_view(['GET'])
def inventario(request):
    productos = Producto.objects.all()
    serializer = ProductoInventarioSerializer(productos, many = True)
        
    return Response(serializer.data)

@api_view(['GET'])
def resumen_pedidos_personalizados(request):
    
    desde = request.query_params.get('desde')
    hasta = request.query_params.get('hasta')
    
    if not desde or not hasta:
        return Response({"error":"Faltan parametros 'desde'  y 'hasta'"}, status = 400)
    
    pedidos = Pedido.objects.filter(fecha__gte = desde, fecha__lte = hasta) 
    ingresos_totales = pedidos.aggregate(ingresos_totales = Sum("total"))['ingresos_totales'] or 0
    total_pedidos = pedidos.count()
    
    resumen = {
        "desde": desde,
        "hasta": hasta,
        "total_pedidos": total_pedidos,
        "ingresos_totales": ingresos_totales,
        "promedio_por_pedidos": ingresos_totales/total_pedidos if total_pedidos else 0
},
        
    return Response(resumen)