from django.conf import settings
from django.db import models
from django.utils.text import slugify


class PerfilCliente(models.Model):
    TIPO_DOC_CHOICES = [
        ('T.I', 'Tarjeta de Identidad'),
        ('C.C', 'Cédula de Ciudadanía'),
        ('C.E', 'Cédula de Extranjería'),
        ('P.A', 'Pasaporte'),
    ]

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil'
    )
    tipo_documento = models.CharField(max_length=3, choices=TIPO_DOC_CHOICES)
    numero_documento = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = 'Perfil de cliente'
        verbose_name_plural = 'Perfiles de clientes'

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username


class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categorías'
        ordering = ['orden', 'nombre']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    STOCK_MINIMO = 3

    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name='productos'
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.CharField(max_length=255, blank=True)
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    vendidos = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['categoria__orden', 'nombre']

    def __str__(self):
        return self.nombre

    @property
    def disponible(self):
        return self.activo and self.stock > 0

    @property
    def precio_formateado(self):
        return f"${self.precio:,.0f}".replace(',', '.')

    @property
    def estado_inventario(self):
        if not self.activo:
            return 'Inactivo'
        if self.stock == 0:
            return 'No disponible'
        if self.stock <= self.STOCK_MINIMO:
            return 'Queda poco'
        return 'Activo'

    @property
    def estado_inventario_clase(self):
        return {
            'Inactivo': 'estado-inactivo',
            'No disponible': 'estado-agotado',
            'Queda poco': 'estado-poco',
            'Activo': 'estado-activo',
        }[self.estado_inventario]


class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('preparacion', 'En preparación'),
        ('listo', 'Listo para recoger'),
        ('completado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pedidos'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f'Pedido #{self.id} - {self.cliente}'

    def siguiente_estado(self):
        orden = ['pendiente', 'preparacion', 'listo', 'completado']
        if self.estado not in orden:
            return None
        idx = orden.index(self.estado)
        if idx + 1 < len(orden):
            return orden[idx + 1]
        return None

    ACCION_POR_ESTADO = {
        'pendiente': 'Enviar a cocina',
        'preparacion': 'Marcar como listo',
        'listo': 'Marcar como entregado',
    }

    @property
    def texto_accion(self):
        return self.ACCION_POR_ESTADO.get(self.estado)


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='items_pedido')
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'
