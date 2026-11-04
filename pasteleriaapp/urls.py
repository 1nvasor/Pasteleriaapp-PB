from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # --- Autenticación web ---
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='pasteleriaapp/login.html',
            redirect_authenticated_user=True,
        ),
        name='login',
    ),
    # Django 5: el logout solo acepta POST (el botón de la barra lo envía así)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # --- Vistas web (requieren sesión) ---
    path('', views.inicio, name='inicio'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),

    # --- API REST (JSON, requieren token salvo /api/login/) ---
    path('api/login/', views.LoginApiView.as_view(), name='api_login'),
    path('api/productos/', views.ProductosApiView.as_view(), name='api_productos'),
    path('api/productos/<int:id>/', views.ProductoDetalleApiView.as_view(), name='api_producto_detalle'),
]
