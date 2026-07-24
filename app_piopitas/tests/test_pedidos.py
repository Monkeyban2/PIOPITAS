import json

from django.test import TestCase
from django.urls import reverse

from app_piopitas.models import ItemPedido, Pedido, Producto
from app_piopitas.tests.factories import crear_cliente, crear_producto


class CrearPedidoTests(TestCase):

    def setUp(self):
        self.url = reverse('crear_pedido')
        self.cliente = crear_cliente()
        self.producto = crear_producto(nombre='Alitas BBQ', precio=18900, stock=10)

    def _post_json(self, payload):
        return self.client.post(self.url, data=json.dumps(payload), content_type='application/json')

    def test_stock_suficiente_descuenta_stock_y_crea_pedido(self):
        # ARRANGE
        self.client.force_login(self.cliente)
        payload = {'items': [{'id': self.producto.id, 'cantidad': 3}]}

        # ACT
        respuesta = self._post_json(payload)

        # ASSERT
        self.producto.refresh_from_db()
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(self.producto.stock, 7)          # 10 - 3
        self.assertEqual(self.producto.vendidos, 3)
        self.assertEqual(Pedido.objects.count(), 1)
        self.assertEqual(ItemPedido.objects.get().cantidad, 3)

    def test_stock_insuficiente_no_modifica_stock_ni_crea_pedido(self):
        # ARRANGE
        self.client.force_login(self.cliente)
        payload = {'items': [{'id': self.producto.id, 'cantidad': 99}]}  # más que el stock (10)

        # ACT
        respuesta = self._post_json(payload)

        # ASSERT
        self.producto.refresh_from_db()
        cuerpo = respuesta.json()
        self.assertEqual(respuesta.status_code, 400)
        self.assertFalse(cuerpo['ok'])
        self.assertEqual(self.producto.stock, 10)          # no cambió
        self.assertEqual(Pedido.objects.count(), 0)         # no quedó pedido a medias

    def test_producto_inactivo_no_se_puede_pedir(self):
        # ARRANGE
        self.client.force_login(self.cliente)
        producto_agotado = crear_producto(nombre='Agotado', stock=5, activo=False)
        payload = {'items': [{'id': producto_agotado.id, 'cantidad': 1}]}

        # ACT
        respuesta = self._post_json(payload)

        # ASSERT
        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Pedido.objects.count(), 0)

    def test_usuario_no_autenticado_no_puede_crear_pedido(self):
        # ARRANGE — sin login
        payload = {'items': [{'id': self.producto.id, 'cantidad': 1}]}

        # ACT
        respuesta = self._post_json(payload)

        # ASSERT
        self.assertEqual(respuesta.status_code, 302)  # redirige a inicioS
        self.assertEqual(Pedido.objects.count(), 0)

    def test_carrito_vacio_retorna_error_sin_crear_pedido(self):
        # ARRANGE
        self.client.force_login(self.cliente)

        # ACT
        respuesta = self._post_json({'items': []})

        # ASSERT
        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Pedido.objects.count(), 0)

    def test_dos_productos_en_el_mismo_pedido_descuenta_stock_de_ambos(self):
        # ARRANGE
        self.client.force_login(self.cliente)
        segundo_producto = crear_producto(nombre='Limonada', precio=7500, stock=20)
        payload = {'items': [
            {'id': self.producto.id, 'cantidad': 2},
            {'id': segundo_producto.id, 'cantidad': 5},
        ]}

        # ACT
        respuesta = self._post_json(payload)

        # ASSERT
        self.producto.refresh_from_db()
        segundo_producto.refresh_from_db()
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(self.producto.stock, 8)
        self.assertEqual(segundo_producto.stock, 15)
        total_esperado = (18900 * 2) + (7500 * 5)
        self.assertEqual(Pedido.objects.get().total, total_esperado)
