from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

EMAIL = 'admin@piopitas.com'
PASSWORD = 'Piopitas123'


class Command(BaseCommand):
    help = 'Crea un superusuario de demostración si todavía no existe.'

    def handle(self, *args, **options):
        if User.objects.filter(username=EMAIL).exists():
            self.stdout.write('El administrador de demostración ya existe.')
            return

        User.objects.create_superuser(username=EMAIL, email=EMAIL, password=PASSWORD)
        self.stdout.write(self.style.SUCCESS(f'Administrador creado -> correo: {EMAIL} | contraseña: {PASSWORD}'))
