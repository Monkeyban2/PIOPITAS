from django.test import TestCase
from django.urls import reverse

from app_piopitas.models import ItemPedido, Pedido, Producto
from app_piopitas.tests.factories import crear_administrador, crear_cliente, crear_producto


class AccesoPanelAdminTests(TestCase):

    def test_usuario_staff_accede_correctamente_al_panel(self):
        # ARRANGE
        admin = crear_administrador()
        self.client.force_login(admin)

        # ACT
        respuesta = self.client.get(reverse('admin_panel'))

        # ASSERT
        self.assertEqual(respuesta.status_code, 200)

    def test_usuario_cliente_no_accede_al_panel_admin(self):
        # ARRANGE
        cliente = crear_cliente()
        self.client.force_login(cliente)

        # ACT
        respuesta = self.client.get(reverse('admin_panel'))

        # ASSERT — user_passes_test redirige (302), no muestra el panel
        self.assertEqual(respuesta.status_code, 302)

    def test_usuario_anonimo_no_accede_al_panel_admin(self):
        # ARRANGE — sin login

        # ACT
        respuesta = self.client.get(reverse('admin_panel'))

        # ASSERT
        self.assertEqual(respuesta.status_code, 302)


class EliminarProductoTests(TestCase):

    def setUp(self):
        self.admin = crear_administrador()
        self.client.force_login(self.admin)

    def test_eliminar_producto_sin_pedidos_lo_borra_de_la_base_de_datos(self):
        # ARRANGE
        producto = crear_producto(nombre='Producto sin pedidos')
        url = reverse('admin_producto_eliminar', args=[producto.id])

        # ACT
        self.client.post(url)

        # ASSERT
        self.assertFalse(Producto.objects.filter(id=producto.id).exists())

    def test_eliminar_producto_con_pedidos_asociados_lo_desactiva_en_vez_de_borrarlo(self):
        # ARRANGE
        cliente = crear_cliente()
        producto = crear_producto(nombre='Producto con historial', activo=True)
        pedido = Pedido.objects.create(cliente=cliente, total=producto.precio)
        ItemPedido.objects.create(pedido=pedido, producto=producto, cantidad=1, precio_unitario=producto.precio)
        url = reverse('admin_producto_eliminar', args=[producto.id])

        # ACT
        self.client.post(url)

        # ASSERT — no se borra (rompería el historial del pedido), se desactiva
        producto.refresh_from_db()
        self.assertTrue(Producto.objects.filter(id=producto.id).exists())
        self.assertFalse(producto.activo)
