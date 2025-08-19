from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# tablas para base de datos

class Producto(models.Model):
    sku_producto = models.CharField(max_length=20, unique=True, db_index=True)
    nombre_producto = models.CharField(max_length=100, db_index=True)
    precio_producto_mxn = models.DecimalField(max_digits=6, decimal_places=2)
    marca = models.CharField(max_length=100, blank=True, null=True)
    creado_por = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="productos_creados")
    creado_fecha = models.DateTimeField(auto_now_add=True)
    modificado_por = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="productos_modificados")
    modificado_fecha = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return self.nombre_producto

# metricas busquedas
class SearchLog(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    query = models.CharField(max_length=255, blank=True, null=True)
    user_session = models.CharField(max_length=100)  # identificador de usuario anonimo

    def __str__(self):
        return f"{self.fecha} - {self.query or 'sin query'}"

# metricas productos vistos
class ViewLog(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    user_session = models.CharField(max_length=100)
    producto = models.ForeignKey("Producto", on_delete=models.CASCADE)
    clicked_buy = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.fecha} - {self.producto.nombre_producto}"
