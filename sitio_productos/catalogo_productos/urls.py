from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_productos, name="lista_productos"),
    path("producto/<int:pk>/", views.ver_producto, name="ver_producto"),
    path("producto/<int:pk>/dummy-buy/", views.producto_dummy_buy, name="producto_dummy_buy"),
]
