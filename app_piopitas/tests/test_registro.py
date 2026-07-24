from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app_piopitas.models import PerfilCliente
from app_piopitas.tests.factories import crear_cliente


class RegistroClienteTests(TestCase):

    def setUp(self):
        self.url = reverse('registro')
        self.datos_validos = {
            'tipo_doc': 'C.C',
            'num_doc': '1122334455',
            'nombres': 'Jhon',
            'apellidos': 'Doe',
            'email': 'jhon.doe@piopitas.com',
            'password': 'ClaveSegura123',
        }

    def test_registro_datos_validos_crea_usuario_y_perfil(self):
        # ARRANGE — self.datos_validos ya preparado en setUp

        # ACT
        respuesta = self.client.post(self.url, self.datos_validos)

        # ASSERT
        usuario = User.objects.get(username='jhon.doe@piopitas.com')
        self.assertTrue(PerfilCliente.objects.filter(usuario=usuario, numero_documento='1122334455').exists())
        self.assertRedirects(respuesta, reverse('menu'))

    def test_registro_email_duplicado_no_crea_segundo_usuario(self):
        # ARRANGE
        crear_cliente(username='jhon.doe@piopitas.com', numero_documento='0000000000')
        total_usuarios_antes = User.objects.count()

        # ACT
        respuesta = self.client.post(self.url, self.datos_validos)

        # ASSERT
        self.assertEqual(User.objects.count(), total_usuarios_antes)
        self.assertEqual(respuesta.status_code, 200)  # vuelve a mostrar el formulario, no redirige

    def test_registro_documento_duplicado_no_crea_segundo_usuario(self):
        # ARRANGE
        crear_cliente(username='otro@piopitas.com', numero_documento='1122334455')
        total_usuarios_antes = User.objects.count()

        # ACT
        respuesta = self.client.post(self.url, self.datos_validos)

        # ASSERT
        self.assertEqual(User.objects.count(), total_usuarios_antes)
        self.assertEqual(respuesta.status_code, 200)

    def test_registro_password_menor_a_8_caracteres_no_crea_usuario(self):
        # ARRANGE
        datos = {**self.datos_validos, 'password': '123'}

        # ACT
        self.client.post(self.url, datos)

        # ASSERT
        self.assertFalse(User.objects.filter(username='jhon.doe@piopitas.com').exists())
