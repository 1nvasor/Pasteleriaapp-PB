from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Producto


def crear_producto_demo(**extra):
    datos = {
        'nombre': 'Torta Amor',
        'categoria': 'Tortas',
        'descripcion': 'Torta de vainilla',
        'precio': 18000,
        'stock': 10,
        'correo_proveedor': 'proveedor@pasteleria.cl',
    }
    datos.update(extra)
    return Producto.objects.create(**datos)


# ------------------------------------------------------------
#  Autenticación y vistas web
# ------------------------------------------------------------
class AutenticacionWebTests(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(username='repostero', password='clave-segura-123')
        self.producto = crear_producto_demo()

    def test_vistas_protegidas_redirigen_al_login(self):
        rutas = [
            reverse('inicio'),
            reverse('crear_producto'),
            reverse('editar_producto', args=[self.producto.id]),
            reverse('eliminar_producto', args=[self.producto.id]),
        ]
        for ruta in rutas:
            resp = self.client.get(ruta)
            self.assertRedirects(
                resp, f"{reverse('login')}?next={ruta}", fetch_redirect_response=False
            )

    def test_login_correcto_inicia_sesion(self):
        resp = self.client.post(
            reverse('login'), {'username': 'repostero', 'password': 'clave-segura-123'}
        )
        self.assertRedirects(resp, reverse('inicio'), fetch_redirect_response=False)
        self.assertEqual(self.client.get(reverse('inicio')).status_code, 200)

    def test_login_incorrecto_no_inicia_sesion(self):
        resp = self.client.post(
            reverse('login'), {'username': 'repostero', 'password': 'mala'}
        )
        self.assertEqual(resp.status_code, 200)          # vuelve al formulario
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(self.client.get(reverse('inicio')).status_code, 302)

    def test_logout_cierra_la_sesion(self):
        self.client.login(username='repostero', password='clave-segura-123')
        resp = self.client.post(reverse('logout'))
        self.assertRedirects(resp, reverse('login'), fetch_redirect_response=False)
        self.assertEqual(self.client.get(reverse('inicio')).status_code, 302)

    def test_logout_por_get_no_esta_permitido(self):
        self.client.login(username='repostero', password='clave-segura-123')
        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)

    def test_usuario_autenticado_ve_el_listado(self):
        self.client.login(username='repostero', password='clave-segura-123')
        resp = self.client.get(reverse('inicio'))
        self.assertContains(resp, 'Torta Amor')
        self.assertContains(resp, 'proveedor@pasteleria.cl')


# ------------------------------------------------------------
#  API REST: GET y POST
# ------------------------------------------------------------
class ApiProductosTests(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(username='repostero', password='clave-segura-123')
        self.token = Token.objects.create(user=self.usuario)
        self.client = APIClient()
        self.url_lista = reverse('api_productos')
        self.datos_validos = {
            'nombre': 'Pie de Limón',
            'categoria': 'Pie',
            'descripcion': 'Con merengue',
            'precio': 12000,
            'stock': 5,
            'correo_proveedor': 'dulces@pasteleria.cl',
        }

    def autenticar(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    # ---- /api/login/ ----
    def test_api_login_correcto_devuelve_token(self):
        resp = self.client.post(
            reverse('api_login'),
            {'username': 'repostero', 'password': 'clave-segura-123'},
            format='json',
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['token'], self.token.key)

    def test_api_login_credenciales_incorrectas_401(self):
        resp = self.client.post(
            reverse('api_login'),
            {'username': 'repostero', 'password': 'mala'},
            format='json',
        )
        self.assertEqual(resp.status_code, 401)

    def test_api_login_sin_datos_400(self):
        resp = self.client.post(reverse('api_login'), {}, format='json')
        self.assertEqual(resp.status_code, 400)

    # ---- Autenticación obligatoria ----
    def test_get_lista_sin_token_401(self):
        self.assertEqual(self.client.get(self.url_lista).status_code, 401)

    def test_post_sin_token_401_y_no_crea_nada(self):
        resp = self.client.post(self.url_lista, self.datos_validos, format='json')
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(Producto.objects.count(), 0)

    def test_token_invalido_401(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token abc123inventado')
        self.assertEqual(self.client.get(self.url_lista).status_code, 401)

    # ---- GET lista ----
    def test_get_lista_devuelve_json_con_datos(self):
        crear_producto_demo()
        crear_producto_demo(nombre='Galleta Chip', categoria='Galletas', precio=1500)
        self.autenticar()
        resp = self.client.get(self.url_lista)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 2)
        self.assertIn('correo_proveedor', resp.json()[0])

    def test_get_lista_vacia(self):
        self.autenticar()
        resp = self.client.get(self.url_lista)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), [])

    # ---- GET por ID ----
    def test_get_por_id_existente(self):
        producto = crear_producto_demo()
        self.autenticar()
        resp = self.client.get(reverse('api_producto_detalle', args=[producto.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['id'], producto.id)
        self.assertEqual(resp.json()['nombre'], 'Torta Amor')

    def test_get_por_id_inexistente_404(self):
        self.autenticar()
        resp = self.client.get(reverse('api_producto_detalle', args=[9999]))
        self.assertEqual(resp.status_code, 404)

    # ---- POST crear ----
    def test_post_crea_producto_y_queda_en_la_base_de_datos(self):
        self.autenticar()
        resp = self.client.post(self.url_lista, self.datos_validos, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Producto.objects.count(), 1)
        creado = Producto.objects.get(id=resp.json()['producto']['id'])
        self.assertEqual(creado.nombre, 'Pie de Limón')
        self.assertEqual(creado.precio, 12000)

    def test_producto_creado_por_api_aparece_en_la_web(self):
        self.autenticar()
        self.client.post(self.url_lista, self.datos_validos, format='json')
        web = self.client_class()
        web.login(username='repostero', password='clave-segura-123')
        self.assertContains(web.get(reverse('inicio')), 'Pie de Limón')

    def test_post_precio_cero_400(self):
        self.autenticar()
        resp = self.client.post(self.url_lista, {**self.datos_validos, 'precio': 0}, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('precio', resp.json())
        self.assertEqual(Producto.objects.count(), 0)

    def test_post_stock_negativo_400(self):
        self.autenticar()
        resp = self.client.post(self.url_lista, {**self.datos_validos, 'stock': -1}, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('stock', resp.json())

    def test_post_correo_invalido_400(self):
        self.autenticar()
        resp = self.client.post(
            self.url_lista, {**self.datos_validos, 'correo_proveedor': 'no-es-correo'}, format='json'
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn('correo_proveedor', resp.json())

    def test_post_categoria_invalida_400(self):
        self.autenticar()
        resp = self.client.post(
            self.url_lista, {**self.datos_validos, 'categoria': 'Pizzas'}, format='json'
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn('categoria', resp.json())

    def test_post_sin_campos_obligatorios_400(self):
        self.autenticar()
        resp = self.client.post(self.url_lista, {'nombre': 'Solo nombre'}, format='json')
        self.assertEqual(resp.status_code, 400)
        for campo in ('precio', 'stock', 'correo_proveedor'):
            self.assertIn(campo, resp.json())

    def test_post_tipo_de_dato_invalido_400(self):
        self.autenticar()
        resp = self.client.post(self.url_lista, {**self.datos_validos, 'precio': 'caro'}, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_post_json_mal_formado_400(self):
        self.autenticar()
        resp = self.client.post(self.url_lista, '{"nombre": ', content_type='application/json')
        self.assertEqual(resp.status_code, 400)
