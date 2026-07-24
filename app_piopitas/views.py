import json
import logging
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .forms import ActualizarStockForm, ProductoForm, RegistroClienteForm
from .models import Categoria, ItemPedido, Pedido, Producto

logger = logging.getLogger(__name__)


def inicio(request):
    return render(request, 'index.html')


def menu(request):
    categorias = Categoria.objects.prefetch_related('productos').all()
    return render(request, 'html/menu.html', {'categorias': categorias})


def resenas(request):
    return render(request, 'html/reseñas.html')


def politica(request):
    return render(request, 'html/pol.html')


def tc(request):
    return render(request, 'html/termcond.html')


def inicioS(request):
    if request.method == 'POST':
        email = request.POST.get('username', '').strip().lower()
        password = request.POST.get('password', '')
        usuario = authenticate(request, username=email, password=password)

        if usuario is None:
            messages.error(request, 'Correo o contraseña incorrectos.')
        elif usuario.is_staff:
            messages.error(request, 'Esta cuenta es de administrador. Ingresa desde el acceso de administrador.')
        else:
            login(request, usuario)
            return redirect('menu')

    return render(request, 'registration/login.html')


def registro(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            usuario = form.guardar()
            login(request, usuario)
            messages.success(request, '¡Cuenta creada con éxito! Bienvenido a Piopitas.')
            return redirect('menu')
    else:
        form = RegistroClienteForm()

    return render(request, 'html/registro.html', {'form': form})


def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')


class RecuperarContrasenaView(auth_views.PasswordResetView):
    template_name = 'html/reccont.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception:
            logger.exception('Error enviando el correo de recuperación de contraseña')
            messages.error(
                self.request,
                'No pudimos enviar el correo en este momento. Intenta de nuevo en unos minutos.',
            )
            return redirect('recuperar')


def es_administrador(usuario):
    return usuario.is_authenticated and usuario.is_staff


def inicioSA(request):
    if request.method == 'POST':
        email = request.POST.get('username', '').strip().lower()
        password = request.POST.get('password', '')
        usuario = authenticate(request, username=email, password=password)

        if usuario is None:
            messages.error(request, 'Correo o contraseña incorrectos.')
        elif not usuario.is_staff:
            messages.error(request, 'Esta cuenta no tiene permisos de administrador.')
        else:
            login(request, usuario)
            return redirect('admin_panel')

    return render(request, 'html/inia.html')


administrador_requerido = user_passes_test(es_administrador, login_url='inicioSA')


@login_required(login_url='inicioS')
@transaction.atomic
def crear_pedido(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Método no permitido.'}, status=405)

    try:
        datos = json.loads(request.body)
        items_carrito = datos.get('items', [])
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({'ok': False, 'error': 'Datos inválidos.'}, status=400)

    if not items_carrito:
        return JsonResponse({'ok': False, 'error': 'El carrito está vacío.'}, status=400)

    pedido = Pedido.objects.create(cliente=request.user, total=0)
    total = Decimal('0')

    for item in items_carrito:
        try:
            producto_id = int(item.get('id'))
            cantidad = int(item.get('cantidad', 1))
        except (TypeError, ValueError):
            transaction.set_rollback(True)
            return JsonResponse({'ok': False, 'error': 'Producto inválido en el carrito.'}, status=400)

        producto = get_object_or_404(Producto, id=producto_id)

        if cantidad < 1:
            transaction.set_rollback(True)
            return JsonResponse({'ok': False, 'error': f'Cantidad inválida para {producto.nombre}.'}, status=400)

        if not producto.activo or producto.stock < cantidad:
            transaction.set_rollback(True)
            return JsonResponse(
                {'ok': False, 'error': f'No hay suficiente stock de "{producto.nombre}".'},
                status=400,
            )

        ItemPedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio,
        )

        producto.stock -= cantidad
        producto.vendidos += cantidad
        producto.save(update_fields=['stock', 'vendidos'])

        total += producto.precio * cantidad

    pedido.total = total
    pedido.save(update_fields=['total'])

    return JsonResponse({'ok': True, 'pedido_id': pedido.id, 'total': str(total)})


@administrador_requerido
def admin(request):
    contexto = {
        'pedidos_pendientes': Pedido.objects.filter(estado='pendiente').count(),
        'productos_registrados': Producto.objects.count(),
        'pedidos_recientes': Pedido.objects.select_related('cliente').all()[:5],
    }
    return render(request, 'html/administrador/administrador.html', contexto)


@administrador_requerido
def adminPro(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado con éxito.')
            return redirect('admin_productos')
    else:
        form = ProductoForm()

    contexto = {
        'productos': Producto.objects.select_related('categoria').all(),
        'form': form,
    }
    return render(request, 'html/administrador/administrador_productos.html', contexto)


@administrador_requerido
def adminProActualizarStock(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ActualizarStockForm(request.POST)
        if form.is_valid():
            producto.stock = form.cleaned_data['stock']
            producto.save(update_fields=['stock'])
            messages.success(request, f'Stock de "{producto.nombre}" actualizado a {producto.stock}.')
        else:
            messages.error(request, 'El stock debe ser un número entero mayor o igual a 0.')
    return redirect('admin_productos')


@administrador_requerido
def adminProEliminar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        try:
            producto.delete()
            messages.success(request, 'Producto eliminado con éxito.')
        except ProtectedError:
            producto.activo = False
            producto.save(update_fields=['activo'])
            messages.warning(
                request,
                'El producto tiene pedidos asociados, así que se desactivó en lugar de eliminarse.',
            )
    return redirect('admin_productos')


@administrador_requerido
def adminPed(request):
    contexto = {'pedidos': Pedido.objects.select_related('cliente').prefetch_related('items__producto').all()}
    return render(request, 'html/administrador/administrador_pedidos.html', contexto)


@administrador_requerido
def adminPedAvanzar(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        siguiente = pedido.siguiente_estado()
        if siguiente:
            pedido.estado = siguiente
            pedido.save(update_fields=['estado'])
    return redirect('admin_pedidos')
