from django.db import models

# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length = 50)
    precio = models.DecimalField(max_digits= 10, decimal_places= 2)
    disponible =  models.BooleanField(default = True)    
    stock = models.PositiveBigIntegerField(default= 0)
    stock_minimo =  models.PositiveBigIntegerField(default = 5)
    
    def __str__(self):
        return self.nombre
    
    def stock_bajo(self):
        return self.stock <= self.stock_minimo
 
class Pedido(models.Model):
    
    cliente = models.CharField(max_length = 100)
    producto = models.ForeignKey(Producto, on_delete= models.PROTECT)
    cantidad =  models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha =  models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.cliente} - {self.producto}"
    
    