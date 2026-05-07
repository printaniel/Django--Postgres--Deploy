from django.test import TestCase
from .models import *
from django.core.exceptions import ValidationError

class TestProductoModel(TestCase):
    
    def test_crear_producto_valido(self):
        # Arrange
        datos = {
            'nombre': "Mouse Gaming",
            'precio': 3500,
            'disponible': True
        }
        
        # Act
        producto = Producto.objects.create(**datos)
        #Assert
        self.assertEqual(producto.nombre, 'Mouse Gaming')
        self.assertEqual(producto.precio, 3500)
        self.assertEqual(producto.disponible, True)
        
    def test_validar_nombre(self):
        
        # Arrange
        producto_invalido = Producto(nombre = '', precio = 3500, disponible = True)
        
        #Assert
        with self.assertRaises(ValidationError) as e:
            producto_invalido.full_clean()
                    
    