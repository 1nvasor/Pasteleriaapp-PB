from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoCrearForm, ProductoEditarForm

# Página principal y Listado
def inicio(request):
    productos = Producto.objects.all().order_by('-fecha_creacion')
    return render(request, 'pasteleriaapp/inicio.html', {'productos': productos})

# Formulario de Crear
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoCrearForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = ProductoCrearForm()
    return render(request, 'pasteleriaapp/crear.html', {'form': form})

# Formulario de Editar
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoEditarForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = ProductoEditarForm(instance=producto)
    return render(request, 'pasteleriaapp/editar.html', {'form': form, 'producto': producto})

# Confirmación y Eliminación
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('inicio')
    return render(request, 'pasteleriaapp/eliminar.html', {'producto': producto})

# En pasteleriaapp/views.py
def inicio(request):
    productos = Producto.objects.all().order_by('-fecha_creacion')
    return render(request, 'pasteleriaapp/inicio.html', {'productos': productos})