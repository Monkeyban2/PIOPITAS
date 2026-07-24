from django.test import TestCase

from app_piopitas.models import ItemPedido, Pedido
from app_piopitas.tests.factories import crear_categoria, crear_cliente, crear_producto


class ProductoDisponibleTests(TestCase):

    def test_disponible_con_stock_y_activo_retorna_true(self):
        # ARRANGE
        producto = crear_producto(stock=5, activo=True)

        # ACT
        resultado = producto.disponible

        # ASSERT
        self.assertTrue(resultado)

    def test_disponible_sin_stock_retorna_false(self):
        # ARRANGE
        producto = crear_producto(stock=0, activo=True)

        # ACT
        resultado = producto.disponible

        # ASSERT
        self.assertFalse(resultado)

    def test_disponible_inactivo_retorna_false(self):
        # ARRANGE
        producto = crear_producto(stock=5, activo=False)

        # ACT
        resultado = producto.disponible

        # ASSERT
        self.assertFalse(resultado)


class ProductoEstadoInventarioTests(TestCase):

    def test_estado_con_stock_normal_retorna_activo(self):
        # ARRANGE
        producto = crear_producto(stock=10, activo=True)

        # ACT
        resultado = producto.estado_inventario

        # ASSERT
        self.assertEqual(resultado, 'Activo')

    def test_estado_con_stock_igual_al_minimo_retorna_queda_poco(self):
        # ARRANGE — el límite (3) también debe contar como "queda poco"
        producto = crear_producto(stock=3, activo=True)

        # ACT
        resultado = producto.estado_inventario

        # ASSERT
        self.assertEqual(resultado, 'Queda poco')

    def test_estado_con_stock_bajo_retorna_queda_poco(self):
        # ARRANGE
        producto = crear_producto(stock=1, activo=True)

        # ACT
        resultado = producto.estado_inventario

        # ASSERT
        self.assertEqual(resultado, 'Queda poco')

    def test_estado_sin_stock_retorna_no_disponible(self):
        # ARRANGE
        producto = crear_producto(stock=0, activo=True)

        # ACT
        resultado = producto.estado_inventario

        # ASSERT
        self.assertEqual(resultado, 'No disponible')

    def test_estado_inactivo_prevalece_sobre_el_stock(self):
        # ARRANGE — aunque tenga stock de sobra, si está inactivo debe decir Inactivo
        producto = crear_producto(stock=50, activo=False)

        # ACT
        resultado = producto.estado_inventario

        # ASSERT
        self.assertEqual(resultado, 'Inactivo')


class CategoriaSlugTests(TestCase):

    def test_guardar_categoria_sin_slug_lo_genera_automaticamente(self):
        # ARRANGE
        categoria = crear_categoria(nombre='Bebidas y Postres')

        # ACT
        slug_generado = categoria.slug

        # ASSERT
        self.assertEqual(slug_generado, 'bebidas-y-postres')


class PedidoSiguienteEstadoTests(TestCase):

    def setUp(self):
        self.cliente = crear_cliente()

    def test_siguiente_estado_desde_pendiente_retorna_preparacion(self):
        # ARRANGE
        pedido = Pedido.objects.create(cliente=self.cliente, estado='pendiente')

        # ACT
        siguiente = pedido.siguiente_estado()

        # ASSERT
        self.assertEqual(siguiente, 'preparacion')

    def test_siguiente_estado_desde_listo_retorna_completado(self):
        # ARRANGE
        pedido = Pedido.objects.create(cliente=self.cliente, estado='listo')

        # ACT
        siguiente = pedido.siguiente_estado()

        # ASSERT
        self.assertEqual(siguiente, 'completado')

    def test_siguiente_estado_desde_completado_retorna_none(self):
        # ARRANGE
        pedido = Pedido.objects.create(cliente=self.cliente, estado='completado')

        # ACT
        siguiente = pedido.siguiente_estado()

        # ASSERT
        self.assertIsNone(siguiente)

    def test_siguiente_estado_desde_cancelado_retorna_none(self):
        # ARRANGE — 'cancelado' no forma parte del flujo normal pendiente->...->completado
        pedido = Pedido.objects.create(cliente=self.cliente, estado='cancelado')

        # ACT
        siguiente = pedido.siguiente_estado()

        # ASSERT
        self.assertIsNone(siguiente)


class ItemPedidoSubtotalTests(TestCase):

    def test_subtotal_calcula_cantidad_por_precio_unitario(self):
        # ARRANGE
        cliente = crear_cliente()
        producto = crear_producto(precio=20000)
        pedido = Pedido.objects.create(cliente=cliente, total=0)
        item = ItemPedido.objects.create(
            pedido=pedido, producto=producto, cantidad=3, precio_unitario=20000
        )

        # ACT
        subtotal = item.subtotal

        # ASSERT
        self.assertEqual(subtotal, 60000)
