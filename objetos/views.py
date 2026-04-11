from django.shortcuts import render
from .models import *
from .serializers import ProductoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
