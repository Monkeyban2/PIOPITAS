# Piopitas

Página web de restaurante hecha con Django: registro e inicio de sesión de clientes y administradores, menú conectado a base de datos, carrito que genera pedidos reales y panel de administrador.

## Cómo correrlo (dentro del dispositivo)

descarga los archivos del repositorio y, desde la carpeta del proyecto, corre el programa según tu sistema operativo:

**Windows:**
```
setup.bat
```

**Mac / Linux:**
```
./setup.sh
```

Esto instala automáticamente todo lo necesario para el funcionamiento de Piopitas

Abre en el navegador: **http://127.0.0.1:8000**

## Cuenta de prueba

**Administrador**:
- Correo: `admin@piopitas.com`
- Contraseña: `Piopitas123`

**Cliente:** puedes registrar uno nuevo desde la página o iniciar sesión con:
- Correo: `estebang2710@gmail.com`
- Contraseña: `contraseña`




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
