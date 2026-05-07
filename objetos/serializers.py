
from rest_framework import serializers
from .models import *

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'disponible', 'stock', 'stock_minimo']
        
        
class PedidoSerializer(serializers.ModelSerializer):
    
    producto_nombre = serializers.StringRelatedField(source = 'producto',read_only = True)
    
    producto = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(),
        write_only=True

    )
    
    class Meta:
        model = Pedido
        fields = ['cliente','producto','producto_nombre', 'cantidad', 'total']
        
        
class ProductoInventarioSerializer(serializers.ModelSerializer):
    
    valor_en_inventario = serializers.SerializerMethodField()
    
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'disponible', 'stock', 'stock_minimo', 'stock_bajo', 'valor_en_inventario']
        
    def get_stock_bajo(self, obj):
        return obj.stock_bajo()
    
    def get_valor_en_inventario(self, obj):
        return obj.stock * obj.precio