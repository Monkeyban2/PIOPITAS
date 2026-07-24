from django.contrib import admin

from .models import Categoria, ItemPedido, PerfilCliente, Pedido, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug', 'orden']
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'stock', 'activo', 'vendidos']
    list_filter = ['categoria', 'activo']
    search_fields = ['nombre']


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'fecha', 'estado', 'total']
    list_filter = ['estado']
    inlines = [ItemPedidoInline]


@admin.register(PerfilCliente)
class PerfilClienteAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo_documento', 'numero_documento']
