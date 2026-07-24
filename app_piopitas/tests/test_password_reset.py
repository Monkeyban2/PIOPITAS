from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from app_piopitas.tests.factories import crear_cliente


class RecuperarContrasenaTests(TestCase):

    def setUp(self):
        self.url = reverse('recuperar')

    @patch('django.core.mail.EmailMultiAlternatives.send')
    def test_email_registrado_envia_correo_de_recuperacion(self, mock_send):
        # ARRANGE — mock_send reemplaza el envío real (no toca ningún servidor SMTP)
        crear_cliente(username='cliente@piopitas.com')

        # ACT
        respuesta = self.client.post(self.url, {'email': 'cliente@piopitas.com'})

        # ASSERT
        mock_send.assert_called_once()
        self.assertRedirects(respuesta, reverse('password_reset_done'))

    @patch('django.core.mail.EmailMultiAlternatives.send')
    def test_email_no_registrado_no_envia_correo(self, mock_send):
        # ARRANGE — no se crea ningún cliente con este correo

        # ACT
        respuesta = self.client.post(self.url, {'email': 'no-existe@piopitas.com'})

        # ASSERT — por seguridad, Django redirige igual mostrando "correo enviado",
        # pero el mock nos permite comprobar que en realidad NO se envió nada
        mock_send.assert_not_called()
        self.assertRedirects(respuesta, reverse('password_reset_done'))
