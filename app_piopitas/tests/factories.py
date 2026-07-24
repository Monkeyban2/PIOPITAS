from django.contrib.auth.models import User

from app_piopitas.models import Categoria, PerfilCliente, Producto


def crear_cliente(username='cliente@piopitas.com', password='ClaveSegura123', numero_documento='1000000001'):
    usuario = User.objects.create_user(username=username, email=username, password=password)
    PerfilCliente.objects.create(
        usuario=usuario,
        tipo_documento='C.C',
        numero_documento=numero_documento,
    )
    return usuario


def crear_administrador(username='admin@piopitas.com', password='ClaveAdmin123'):
    return User.objects.create_superuser(username=username, email=username, password=password)


def crear_categoria(nombre='Entradas'):
    return Categoria.objects.create(nombre=nombre)


def crear_producto(categoria=None, nombre='Alitas BBQ', precio=18900, stock=10, activo=True):
    if categoria is None:
        categoria = crear_categoria()
    return Producto.objects.create(
        categoria=categoria,
        nombre=nombre,
        precio=precio,
        stock=stock,
        activo=activo,
    )
