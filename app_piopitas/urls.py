from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('menu', views.menu, name='menu'),
    path('resenas', views.resenas, name='resenas'),
    path('inicioS', views.inicioS, name='inicioS'),
    path('inicioSA', views.inicioSA, name='inicioSA'),
    path('politpriv', views.politica, name='politica'),
    path('registro', views.registro, name='registro'),
    path('termCond', views.tc, name='termCond'),
    path('logout', views.cerrar_sesion, name='logout'),

    path('recContr', auth_views.PasswordResetView.as_view(
        template_name='html/reccont.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        success_url=reverse_lazy('password_reset_done'),
    ), name='recuperar'),
    path('recContr/enviado', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html',
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url=reverse_lazy('password_reset_complete'),
    ), name='password_reset_confirm'),
    path('reset/listo', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html',
    ), name='password_reset_complete'),

    path('pedido/crear', views.crear_pedido, name='crear_pedido'),

    path('admin/', views.admin, name='admin_panel'),
    path('admin/pro', views.adminPro, name='admin_productos'),
    path('admin/pro/<int:producto_id>/stock', views.adminProActualizarStock, name='admin_producto_stock'),
    path('admin/pro/<int:producto_id>/eliminar', views.adminProEliminar, name='admin_producto_eliminar'),
    path('admin/ped', views.adminPed, name='admin_pedidos'),
    path('admin/ped/<int:pedido_id>/avanzar', views.adminPedAvanzar, name='admin_pedido_avanzar'),
]
