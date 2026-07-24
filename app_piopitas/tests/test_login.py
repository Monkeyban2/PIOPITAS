from django.test import TestCase
from django.urls import reverse

from app_piopitas.tests.factories import crear_administrador, crear_cliente


class LoginClienteTests(TestCase):

    def setUp(self):
        self.url = reverse('inicioS')
        self.cliente = crear_cliente(username='cliente@piopitas.com', password='ClaveSegura123')

    def test_login_credenciales_validas_redirige_a_menu(self):
        # ARRANGE — self.cliente ya creado en setUp

        # ACT
        respuesta = self.client.post(self.url, {
            'username': 'cliente@piopitas.com',
            'password': 'ClaveSegura123',
        })

        # ASSERT
        self.assertRedirects(respuesta, reverse('menu'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_password_incorrecta_no_inicia_sesion(self):
        # ARRANGE — self.cliente ya creado en setUp

        # ACT
        respuesta = self.client.post(self.url, {
            'username': 'cliente@piopitas.com',
            'password': 'clave-equivocada',
        })

        # ASSERT
        self.assertEqual(respuesta.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_con_cuenta_de_administrador_rechaza_acceso_por_esta_puerta(self):
        # ARRANGE
        crear_administrador(username='admin@piopitas.com', password='ClaveAdmin123')

        # ACT
        respuesta = self.client.post(self.url, {
            'username': 'admin@piopitas.com',
            'password': 'ClaveAdmin123',
        })

        # ASSERT
        self.assertEqual(respuesta.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)


class LoginAdministradorTests(TestCase):

    def setUp(self):
        self.url = reverse('inicioSA')
        self.admin = crear_administrador(username='admin@piopitas.com', password='ClaveAdmin123')

    def test_login_credenciales_validas_redirige_a_panel_admin(self):
        # ARRANGE — self.admin ya creado en setUp

        # ACT
        respuesta = self.client.post(self.url, {
            'username': 'admin@piopitas.com',
            'password': 'ClaveAdmin123',
        })

        # ASSERT
        self.assertRedirects(respuesta, reverse('admin_panel'))

    def test_login_con_cuenta_de_cliente_rechaza_acceso_por_esta_puerta(self):
        # ARRANGE
        crear_cliente(username='cliente@piopitas.com', password='ClaveSegura123')

        # ACT
        respuesta = self.client.post(self.url, {
            'username': 'cliente@piopitas.com',
            'password': 'ClaveSegura123',
        })

        # ASSERT
        self.assertEqual(respuesta.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
