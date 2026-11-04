from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoCrearForm, ProductoEditarForm

# Imports necesarios para la API REST
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductoSerializer

# ==========================================
# 1. VISTAS HTML (Para la web tradicional)
# ==========================================

def inicio(request):
    productos = Producto.objects.all().order_by('-fecha_creacion')
    return render(request, 'pasteleriaapp/inicio.html', {'productos': productos})

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoCrearForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = ProductoCrearForm()
    return render(request, 'pasteleriaapp/crear.html', {'form': form})

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

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('inicio')
    return render(request, 'pasteleriaapp/eliminar.html', {'producto': producto})


# ==========================================
# 2. VISTAS API REST (Para la evaluación)
# ==========================================

# GET (listar) y POST (crear)
@api_view(['GET', 'POST'])
def api_productos_list(request):
    if request.method == 'GET':
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET (detalle), PUT (actualizar) y DELETE (eliminar)
@api_view(['GET', 'PUT', 'DELETE'])
def api_producto_detail(request, pk):
    # Retorna un error 404 automático si el ID no existe en MySQL
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'GET':
        serializer = ProductoSerializer(producto)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        producto.delete()
        return Response({'message': 'Producto eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)