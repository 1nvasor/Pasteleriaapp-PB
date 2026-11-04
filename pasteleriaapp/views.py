from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from .models import Producto
from .forms import ProductoCrearForm, ProductoEditarForm
from .serializers import ProductoSerializer


# Página principal y Listado
@login_required
def inicio(request):
    productos = Producto.objects.all().order_by('-fecha_creacion')
    return render(request, 'pasteleriaapp/inicio.html', {'productos': productos})


# Formulario de Crear
@login_required
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
@login_required
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
@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('inicio')
    return render(request, 'pasteleriaapp/eliminar.html', {'producto': producto})


# ============================================================
#  API REST (JSON) - autenticación por token
# ============================================================

class LoginApiView(APIView):
    """
    POST /api/login/
    Recibe {"username": "...", "password": "..."} y devuelve el token.
    Es la única ruta de la API que no exige token.
    """

    authentication_classes = []          # no se pide token para obtener el token
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Debes enviar username y password'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        usuario = authenticate(username=username, password=password)

        if usuario is None:
            return Response(
                {'error': 'Usuario o contraseña incorrectos'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, _ = Token.objects.get_or_create(user=usuario)

        return Response(
            {
                'mensaje': 'Autenticación correcta',
                'usuario': usuario.username,
                'token': token.key,
            },
            status=status.HTTP_200_OK,
        )


class ProductosApiView(APIView):
    """
    GET  /api/productos/  -> lista todos los productos
    POST /api/productos/  -> crea un producto nuevo
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # GET: listar
    def get(self, request):
        productos = Producto.objects.all().order_by('-fecha_creacion')
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST: crear
    def post(self, request):
        serializer = ProductoSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        producto = serializer.save()

        return Response(
            {
                'mensaje': 'Producto creado correctamente',
                'producto': ProductoSerializer(producto).data,
            },
            status=status.HTTP_201_CREATED,
        )


class ProductoDetalleApiView(APIView):
    """
    GET    /api/productos/<id>/  -> consulta un producto por ID
    PUT    /api/productos/<id>/  -> actualiza un producto existente (todos los campos)
    DELETE /api/productos/<id>/  -> elimina un producto existente
    Si el ID no existe responde 404 en JSON.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_producto(self, id):
        """Devuelve el producto o None si no existe."""
        try:
            return Producto.objects.get(id=id)
        except Producto.DoesNotExist:
            return None

    def respuesta_no_encontrado(self, id):
        return Response(
            {'error': f'No existe un producto con id {id}'},
            status=status.HTTP_404_NOT_FOUND,
        )

    # GET: consultar por ID
    def get(self, request, id):
        producto = self.get_producto(id)
        if producto is None:
            return self.respuesta_no_encontrado(id)
        return Response(ProductoSerializer(producto).data, status=status.HTTP_200_OK)

    # PUT: actualizar por ID
    def put(self, request, id):
        producto = self.get_producto(id)
        if producto is None:
            return self.respuesta_no_encontrado(id)

        # PUT reemplaza el recurso completo, por eso partial=False:
        # los campos obligatorios deben venir en el JSON.
        serializer = ProductoSerializer(producto, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        producto = serializer.save()

        return Response(
            {
                'mensaje': 'Producto actualizado correctamente',
                'producto': ProductoSerializer(producto).data,
            },
            status=status.HTTP_200_OK,
        )

    # DELETE: eliminar por ID
    def delete(self, request, id):
        producto = self.get_producto(id)
        if producto is None:
            return self.respuesta_no_encontrado(id)

        nombre = producto.nombre
        producto.delete()

        return Response(
            {'mensaje': f'Producto "{nombre}" eliminado correctamente'},
            status=status.HTTP_200_OK,
        )