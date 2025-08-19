from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, SearchLog, ViewLog
from django.db.models import Q

# Create your views here.

def lista_productos(request):
    #get anon id
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    query = request.GET.get("q", "").strip() if request.GET.get("q") else None

    productos = Producto.objects.all()

    if query:
        try:
            # busqueda de producto
            producto = Producto.objects.get(
                Q(nombre_producto=query) | Q(sku_producto=query)
            )
            return redirect("ver_producto", pk=producto.pk)
        except Producto.DoesNotExist:
            productos = Producto.objects.all()
            return render(request, "catalogo_productos/lista_productos.html", {
                "productos": productos,
                "mensaje": f"No se encontró ningún producto con el siguiente SKU o Nombre: '{query}'."
            })

    # si no hay query mostrar lista normal
    productos = Producto.objects.all()
    return render(request, "catalogo_productos/lista_productos.html", {"productos": productos})


def ver_producto(request, pk):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    producto = get_object_or_404(Producto, pk=pk)

    # Guardar log de vista
    ViewLog.objects.create(user_session=session_id, producto=producto)

    return render(request, "catalogo_productos/producto.html", {"producto": producto})

def producto_dummy_buy(request, pk):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    producto = get_object_or_404(Producto, pk=pk)

    # Actualizar log de vista campo Cliecked_buy
    viewlog = ViewLog.objects.filter(user_session=session_id, producto=producto).last()
    if viewlog:
        viewlog.clicked_buy = True
        viewlog.save()


    # Regresar a pag principal
    return redirect("../../../", pk=pk)
