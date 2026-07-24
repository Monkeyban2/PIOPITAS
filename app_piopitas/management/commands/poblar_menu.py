from django.core.management.base import BaseCommand

from app_piopitas.models import Categoria, Producto

CATEGORIAS = [
    ('Entradas', 'entradas', 1),
    ('Hamburguesas', 'hamburguesas', 2),
    ('Platos Fuertes', 'platos_fuertes', 3),
    ('Ensaladas', 'ensaladas', 4),
    ('Bebidas y Postres', 'bebidas_postres', 5),
]

PRODUCTOS = [
    ('entradas', 'Alitas Picantes', '12 Alitas de Pollo bañadas en salsa BBQ.', 18900,
     'img_menu/entradas/alitas_bbq.webp', 30),
    ('entradas', 'Empanadas Artesanales', '6 Unidades de empanadas de pollo con ají', 18900,
     'img_menu/entradas/empanadas_artesanales.webp', 30),
    ('entradas', 'Papas Rústicas', 'Porción grande de papas con cáscara y finas hierbas', 14200,
     'img_menu/entradas/empanadas_rusticas.webp', 30),
    ('entradas', 'Dedos de Queso', '6 bastones de queso mozzarella apanados', 11000,
     'img_menu/entradas/dedos_queso.webp', 30),
    ('entradas', 'Chorizo al Carbón', 'Chorizo artesanal servido con arepas pequeñas y limón', 11000,
     'img_menu/entradas/chorizo.webp', 30),

    ('hamburguesas', 'Hamburguesa Clásica',
     'Carne de res (150g), queso cheddar, lechuga, tomate, cebolla y mayonesa.', 22500,
     'img_menu/hamburguesas/hamburguesa_clasica.webp', 30),
    ('hamburguesas', 'Hamburguesa de Pollo',
     'Pechuga de pollo empanizada, queso suizo, tocineta, lechuga y salsa de la casa.', 24900,
     'img_menu/hamburguesas/hamburguesa_crispy.webp', 30),
    ('hamburguesas', 'Hamburguesa BBQ',
     'Carne de res, aros de cebolla, tocineta, queso cheddar y salsa barbacoa.', 26500,
     'img_menu/hamburguesas/hamburguesa_bbq.webp', 30),
    ('hamburguesas', 'Hamburguesa Saludable',
     'Legumbres y vegetales, aguacate, queso fresco, espinaca y tomate.', 23900,
     'img_menu/hamburguesas/hamburguesa_vegetariana.webp', 30),
    ('hamburguesas', 'Hamburguesa Doble',
     'Dos carnes de res, doble porción de queso cheddar, pepinillos y mostaza.', 28900,
     'img_menu/hamburguesas/hamburguesa_doble_carne.webp', 30),

    ('platos_fuertes', 'Pollo Asado',
     'Un cuarto de pollo asado al carbón, servido con arroz, ensalada fresca y arepa.', 25000,
     'img_menu/platos_fuertes/pollo_asado.webp', 30),
    ('platos_fuertes', 'Pechuga a la Plancha',
     'Pechuga sellada a la parrilla, acompañada de vegetales salteados y puré de papa.', 23500,
     'img_menu/platos_fuertes/pechuga_plancha.webp', 30),
    ('platos_fuertes', 'Pasta a la Carbonara',
     'Fetuccini con salsa blanca, tocineta crujiente y queso parmesano.', 21900,
     'img_menu/platos_fuertes/pasta_carbonara.webp', 30),
    ('platos_fuertes', 'Lomo de Cerdo', 'Corte de cerdo acompañado de ensalada y yuca frita.', 27500,
     'img_menu/platos_fuertes/cerdo.webp', 30),
    ('platos_fuertes', 'Bowl de Pollo',
     'Pollo desmechado, aguacate, maíz tierno, arroz, frijol negro y pico de gallo.', 22000,
     'img_menu/platos_fuertes/bowl_pollo.webp', 30),
    ('platos_fuertes', 'Milanesa de pollo',
     'Pechuga empanizada, cubierta con salsa de pomodoro y queso gratinado con pasta.', 24500,
     'img_menu/platos_fuertes/milanesa.webp', 30),

    ('ensaladas', 'Ensalada César', 'Lechuga romana, crutones, queso parmesano y aderezo césar.', 18500,
     'img_menu/ensaladas/ensalada_cesar.webp', 30),
    ('ensaladas', 'Ensalada de la Casa', 'Lechuga, tomate, zanahoria, pepino y vinagreta cítrica.', 15500,
     'img_menu/ensaladas/ensalada_casa.webp', 30),
    ('ensaladas', 'Ensalada de Quinoa', 'Quinoa, aguacate, tomate cherry, pepino y vinagreta de limón.', 19900,
     'img_menu/ensaladas/ensalada_quinoa.webp', 30),

    ('bebidas_postres', 'Jugo de Maracuyá', 'Fruta del día preparado en agua', 6500,
     'img_menu/bebidas_postres/jugo_maracuya.webp', 50),
    ('bebidas_postres', 'Jugo de Mora', 'Fruta del día preparado en agua', 6500,
     'img_menu/bebidas_postres/jugo_mora.webp', 50),
    ('bebidas_postres', 'Jugo de Lulo', 'Fruta del día preparado en agua', 6500,
     'img_menu/bebidas_postres/jugo_lulo.webp', 50),
    ('bebidas_postres', 'Limonada Natural', 'Limones del día', 7500,
     'img_menu/bebidas_postres/limonada_natural.webp', 50),
    ('bebidas_postres', 'Limonada Cerezada', 'Cerezas del día', 7500,
     'img_menu/bebidas_postres/limonada_cerezada.webp', 50),
    ('bebidas_postres', 'Gaseosa de Manzana', 'Línea de bebidas frescas.', 5000,
     'img_menu/bebidas_postres/gaseosa_manzana.webp', 50),
    ('bebidas_postres', 'Gaseosa de Mora', 'Línea de bebidas frescas.', 5000,
     'img_menu/bebidas_postres/gaseosa_mora.webp', 50),
    ('bebidas_postres', 'Gaseosa de Naranja', 'Línea de bebidas frescas.', 5000,
     'img_menu/bebidas_postres/gaseosa_naranja.webp', 50),
    ('bebidas_postres', 'Brownie', 'Brownie con helado', 9500,
     'img_menu/bebidas_postres/brownie.webp', 50),
]


class Command(BaseCommand):
    help = 'Crea las categorías y productos iniciales del menú de Piopitas.'

    def handle(self, *args, **options):
        slug_a_categoria = {}
        for nombre, slug, orden in CATEGORIAS:
            categoria, creada = Categoria.objects.get_or_create(
                slug=slug, defaults={'nombre': nombre, 'orden': orden}
            )
            slug_a_categoria[slug] = categoria
            if creada:
                self.stdout.write(self.style.SUCCESS(f'Categoría creada: {nombre}'))

        creados = 0
        for slug_cat, nombre, descripcion, precio, imagen, stock in PRODUCTOS:
            _, creado = Producto.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'categoria': slug_a_categoria[slug_cat],
                    'descripcion': descripcion,
                    'precio': precio,
                    'imagen': imagen,
                    'stock': stock,
                    'activo': True,
                },
            )
            if creado:
                creados += 1

        self.stdout.write(self.style.SUCCESS(f'{creados} productos nuevos creados.'))
        self.stdout.write(self.style.SUCCESS('¡Listo! El menú ya está en la base de datos.'))
