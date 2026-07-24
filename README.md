# Piopitas

Página web de restaurante hecha con Django: registro e inicio de sesión de clientes y administradores, menú conectado a base de datos, carrito que genera pedidos reales y panel de administrador.

## Requisitos

- [Python 3.10 o superior](https://www.python.org/downloads/) instalado (en Windows, marca la casilla "Add Python to PATH" durante la instalación).
- Git (para clonar el repositorio).

## Cómo correrlo (una sola vez)

Clona el repositorio y, desde la carpeta del proyecto, corre el script según tu sistema operativo:

**Windows:**
```
setup.bat
```

**Mac / Linux:**
```
./setup.sh
```

Esto instala automáticamente todo lo necesario: crea el entorno virtual, instala Django, prepara la base de datos, carga el menú y crea un administrador de prueba. Al final abre el servidor solo.

Abre en el navegador: **http://127.0.0.1:8000**

## Cuentas de prueba

**Administrador** (http://127.0.0.1:8000/inicioSA):
- Correo: `admin@piopitas.com`
- Contraseña: `Piopitas123`

**Cliente:** puedes registrar uno nuevo desde la página, o iniciar sesión con uno que ya hayas creado antes.

## Volver a levantar el servidor otro día

Ya no hace falta correr el script completo de nuevo. Solo:

**Windows:**
```
venv\Scripts\activate
python manage.py runserver
```

**Mac / Linux:**
```
source venv/bin/activate
python manage.py runserver
```

## Pruebas unitarias

El proyecto tiene 25 pruebas unitarias (modelos, registro, login, pedidos, panel admin,
recuperación de contraseña) en `app_piopitas/tests/`.

Para correrlas:
```
pip install -r requirements-dev.txt
python manage.py test app_piopitas.tests -v 2
```

Para ver el porcentaje de código cubierto:
```
coverage run manage.py test app_piopitas.tests
coverage report -m
coverage html
```
(`coverage html` genera una carpeta `htmlcov/` — abre `htmlcov/index.html` en el navegador
para ver línea por línea qué quedó cubierto).

El reporte de ejecución (resultados, cobertura, defectos encontrados durante el desarrollo)
está en [`REPORTE_PRUEBAS.md`](REPORTE_PRUEBAS.md).

## Despliegue en internet (Render)

El proyecto ya está listo para publicarse gratis en [Render](https://render.com):

1. Entra a render.com e inicia sesión con tu cuenta de GitHub.
2. **New +** → **Web Service** → selecciona tu repositorio de Piopitas.
3. Configura:
   - **Runtime:** Python 3
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn pr_piopitas.wsgi`
   - **Instance Type:** Free
4. Click en **Create Web Service** y espera a que termine el build (unos minutos).
5. Cuando termine, Render te da una URL pública como `https://piopitas.onrender.com` — esa es la dirección web para tu entrega.

El `build.sh` instala dependencias, prepara los archivos estáticos, corre las migraciones, carga el menú y crea el administrador de prueba automáticamente en cada despliegue.

**Cuentas para la entrega:**
- **Administrador:** `admin@piopitas.com` / `Piopitas123`
- **Cliente:** regístrate desde el botón "Sesión" → "Regístrate" en el sitio ya desplegado (o usa uno que ya hayas creado)

⚠️ El plan gratuito de Render "duerme" el sitio tras 15 minutos sin visitas (la primera carga después de eso tarda ~30-50 segundos en despertar) y su almacenamiento es temporal — si el servicio se reinicia, la base de datos vuelve al estado del último despliegue (menú + admin, sin los pedidos/clientes que se hayan creado mientras tanto). Para una presentación en vivo esto no es un problema, solo ten en cuenta que si necesitas datos permanentes a largo plazo, tocaría pasar a una base de datos externa (por ejemplo PostgreSQL, que Render también ofrece gratis).

## Estructura del proyecto

- `app_piopitas/` — aplicación principal (modelos, vistas, urls, formularios)
- `pr_piopitas/` — configuración del proyecto Django
- `templates/` — plantillas HTML
- `app_piopitas/static/` — CSS, JS e imágenes
