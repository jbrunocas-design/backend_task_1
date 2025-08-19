from django.contrib import admin
from .models import Producto, SearchLog, ViewLog
# Register your models here.

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if change:
            try:
                old_obj = Producto.objects.get(pk=obj.pk)
                obj._old_values = {
                    "nombre_producto": old_obj.nombre_producto,
                    "precio_producto_mxn": old_obj.precio_producto_mxn,
                    "marca": old_obj.marca,
                }
            except Producto.DoesNotExist:
                obj._old_values = {}
        else:
            obj._old_values = {}
        obj._actor = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj._actor = request.user
        super().delete_model(request, obj)


@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ("fecha", "query", "user_session")


@admin.register(ViewLog)
class ViewLogAdmin(admin.ModelAdmin):
    list_display = ("fecha", "producto", "user_session", "clicked_buy")
